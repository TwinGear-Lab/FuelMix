import flet as ft
import json
from datetime import datetime
from history_storage import add_history_record
from theme import constrain_width
import os
import asyncio

# Путь к файлу с данными (как в fuelSettingsUserPage)
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataAGS.json")


class RealNumberInputFilter(ft.InputFilter):
    """Фильтр для ввода чисел с плавающей точкой"""

    def __init__(self, allow_negative=False, max_decimals=3):
        self.allow_negative = allow_negative
        self.max_decimals = max_decimals
        # Передаем regex_string в конструктор
        super().__init__(
            regex_string=r"^[0-9]*\.?[0-9]*$",
            allow=True
        )

    def filter(self, value: str) -> str:
        if not value:
            return value

        # Разрешенные символы
        allowed_chars = '0123456789.'
        if self.allow_negative:
            allowed_chars += '-'

        # Фильтруем
        filtered = ''.join(c for c in value if c in allowed_chars)

        # Обработка отрицательных чисел
        if self.allow_negative:
            # '-' только в начале
            if filtered and filtered[0] != '-' and '-' in filtered:
                filtered = filtered.replace('-', '')
            if filtered and filtered[0] == '-':
                filtered = '-' + filtered[1:].replace('-', '')
        else:
            filtered = filtered.replace('-', '')

        # Обработка десятичной точки
        if filtered.count('.') > 1:
            parts = filtered.split('.')
            filtered = parts[0] + '.' + ''.join(parts[1:])

        # Ограничение знаков после запятой
        if self.max_decimals is not None and '.' in filtered:
            int_part, dec_part = filtered.split('.')
            dec_part = dec_part[:self.max_decimals]
            filtered = f"{int_part}.{dec_part}"

        return filtered


def view(page: ft.Page):
    # Загружаем данные АЗС
    data_ags = {}
    gas_stations_rf = []

    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data_ags = json.load(file)
                gas_stations_rf = list(data_ags.keys())
    except Exception as e:
        print(f"Ошибка загрузки данных АЗС: {e}")

    # Создаем фильтр для чисел
    real_filter = RealNumberInputFilter(allow_negative=False, max_decimals=3)

    # Функция для обновления списка топлива при выборе АЗС
    def update_fuel_types(e, dropdown_azs, dropdown_fuel, octane_field):
        """Обновляет список топлива при выборе АЗС"""
        station_name = dropdown_azs.value
        print(f"Выбрана АЗС: {station_name}")

        if station_name and station_name in data_ags:
            fuels = list(data_ags[station_name].keys())
            print(f"Найдено топливо: {fuels}")

            dropdown_fuel.options = [ft.dropdown.Option(fuel) for fuel in fuels]
            dropdown_fuel.value = None
            octane_field.value = ""
            page.update()

    # Функция для автоматической подстановки октанового числа
    def auto_fill_octane(e, dropdown_azs, dropdown_fuel, octane_field):
        """Автоматически подставляет октановое число при выборе топлива"""
        station_name = dropdown_azs.value
        fuel_name = dropdown_fuel.value
        print(f"Выбрано топливо: {fuel_name} для АЗС: {station_name}")

        if station_name and fuel_name and station_name in data_ags:
            if fuel_name in data_ags[station_name]:
                octane_value = data_ags[station_name][fuel_name]
                octane_field.value = str(octane_value)
                page.update()

    # Функция для отображения/скрытия блока топлива в баке
    def toggle_tank_visible(e):
        """Показывает или скрывает блок топлива в баке"""
        if tank_checkbox.value:
            tank_container.visible = True
        else:
            tank_container.visible = False
            # Очищаем поля при скрытии
            tank_azs.value = None
            tank_fuel_type.value = None
            tank_fuel_type.options = []
            tank_octane.value = ""
            tank_volume.value = ""
        page.update()

    # Создаем поля ввода
    # Топливо в баке
    tank_checkbox = ft.Checkbox(
        value=False,
        on_change=toggle_tank_visible,
    )

    # Контейнер для топлива в баке (скрыт по умолчанию)
    tank_container = ft.Container(
        visible=False,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        tank_azs := ft.Dropdown(
                            expand=True,
                            label="АЗС",
                            hint_text="Выберите АЗС",
                            options=[ft.dropdown.Option(station) for station in gas_stations_rf],
                        ),
                        tank_fuel_type := ft.Dropdown(
                            expand=True,
                            label="Тип топлива",
                            hint_text="Выберите топливо",
                            options=[],
                        ),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    controls=[
                        tank_octane := ft.TextField(
                            expand=True,
                            hint_text="Октановое число",
                            suffix=ft.Text("ОЧ"),
                            keyboard_type=ft.KeyboardType.NUMBER,
                            filled=True,
                            input_filter=real_filter,
                        ),
                        tank_volume := ft.TextField(
                            expand=True,
                            hint_text="Объем топлива",
                            suffix=ft.Text("л"),
                            keyboard_type=ft.KeyboardType.NUMBER,
                            filled=True,
                            input_filter=real_filter,
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        ),
    )

    # Привязываем события для tank
    if hasattr(tank_azs, 'on_select'):
        tank_azs.on_select = lambda e: update_fuel_types(e, tank_azs, tank_fuel_type, tank_octane)
    else:
        try:
            tank_azs.on_change = lambda e: update_fuel_types(e, tank_azs, tank_fuel_type, tank_octane)
        except:
            pass

    if hasattr(tank_fuel_type, 'on_select'):
        tank_fuel_type.on_select = lambda e: auto_fill_octane(e, tank_azs, tank_fuel_type, tank_octane)
    else:
        try:
            tank_fuel_type.on_change = lambda e: auto_fill_octane(e, tank_azs, tank_fuel_type, tank_octane)
        except:
            pass

    # Топливо для заправки №1 (октановое число только для чтения)
    fuel1_column = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    fuel1_azs := ft.Dropdown(
                        expand=True,
                        label="АЗС",
                        hint_text="Выберите АЗС",
                        options=[ft.dropdown.Option(station) for station in gas_stations_rf],
                    ),
                    fuel1_type := ft.Dropdown(
                        expand=True,
                        label="Тип топлива",
                        hint_text="Выберите топливо",
                        options=[],
                    ),
                ],
                spacing=10,
            ),
            ft.Row(
                controls=[
                    fuel1_octane := ft.TextField(
                        expand=True,
                        hint_text="Октановое число",
                        suffix=ft.Text("ОЧ"),
                        keyboard_type=ft.KeyboardType.NUMBER,
                        filled=True,
                        read_only=True,
                    ),
                    fuel1_volume := ft.TextField(
                        expand=True,
                        hint_text="Объем топлива",
                        suffix=ft.Text("л"),
                        keyboard_type=ft.KeyboardType.NUMBER,
                        filled=True,
                        input_filter=real_filter,
                    ),
                ],
                spacing=10,
            ),
        ],
        spacing=8,
    )

    if hasattr(fuel1_azs, 'on_select'):
        fuel1_azs.on_select = lambda e: update_fuel_types(e, fuel1_azs, fuel1_type, fuel1_octane)
    else:
        try:
            fuel1_azs.on_change = lambda e: update_fuel_types(e, fuel1_azs, fuel1_type, fuel1_octane)
        except:
            pass

    if hasattr(fuel1_type, 'on_select'):
        fuel1_type.on_select = lambda e: auto_fill_octane(e, fuel1_azs, fuel1_type, fuel1_octane)
    else:
        try:
            fuel1_type.on_change = lambda e: auto_fill_octane(e, fuel1_azs, fuel1_type, fuel1_octane)
        except:
            pass

    # Топливо для заправки №2 (октановое число только для чтения)
    fuel2_column = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    fuel2_azs := ft.Dropdown(
                        expand=True,
                        label="АЗС",
                        hint_text="Выберите АЗС",
                        options=[ft.dropdown.Option(station) for station in gas_stations_rf],
                    ),
                    fuel2_type := ft.Dropdown(
                        expand=True,
                        label="Тип топлива",
                        hint_text="Выберите топливо",
                        options=[],
                    ),
                ],
                spacing=10,
            ),
            ft.Row(
                controls=[
                    fuel2_octane := ft.TextField(
                        expand=True,
                        hint_text="Октановое число",
                        suffix=ft.Text("ОЧ"),
                        keyboard_type=ft.KeyboardType.NUMBER,
                        filled=True,
                        read_only=True,
                    ),
                    fuel2_volume := ft.TextField(
                        expand=True,
                        hint_text="Объем топлива",
                        suffix=ft.Text("л"),
                        keyboard_type=ft.KeyboardType.NUMBER,
                        filled=True,
                        input_filter=real_filter,
                    ),
                ],
                spacing=10,
            ),
        ],
        spacing=8,
    )

    if hasattr(fuel2_azs, 'on_select'):
        fuel2_azs.on_select = lambda e: update_fuel_types(e, fuel2_azs, fuel2_type, fuel2_octane)
    else:
        try:
            fuel2_azs.on_change = lambda e: update_fuel_types(e, fuel2_azs, fuel2_type, fuel2_octane)
        except:
            pass

    if hasattr(fuel2_type, 'on_select'):
        fuel2_type.on_select = lambda e: auto_fill_octane(e, fuel2_azs, fuel2_type, fuel2_octane)
    else:
        try:
            fuel2_type.on_change = lambda e: auto_fill_octane(e, fuel2_azs, fuel2_type, fuel2_octane)
        except:
            pass

    # Результат
    result_octane = ft.TextField(
        expand=True,
        hint_text="Октановое число",
        suffix=ft.Text("ОЧ"),
        keyboard_type=ft.KeyboardType.NUMBER,
        filled=True,
        read_only=True,
    )
    result_volume = ft.TextField(
        expand=True,
        hint_text="Объем топлива",
        suffix=ft.Text("л"),
        keyboard_type=ft.KeyboardType.NUMBER,
        filled=True,
        read_only=True,
    )

    def calculate_mixture(e):
        """Рассчитывает смесь топлива и сохраняет в историю"""
        try:
            # Получаем значения для топлива в баке (если чекбокс активен)
            if tank_checkbox.value:
                octane_tank = float(tank_octane.value) if tank_octane.value else 0
                volume_tank = float(tank_volume.value) if tank_volume.value else 0
                fuel_tank_type = tank_fuel_type.value if tank_fuel_type.value else "Не выбран"
                fuel_tank_azs = tank_azs.value if tank_azs.value else "Не выбрана"
            else:
                octane_tank = 0
                volume_tank = 0
                fuel_tank_type = "Не выбран"
                fuel_tank_azs = "Не выбрана"

            octane_1 = float(fuel1_octane.value) if fuel1_octane.value else 0
            volume_1 = float(fuel1_volume.value) if fuel1_volume.value else 0
            fuel1_type_value = fuel1_type.value if fuel1_type.value else "Не выбран"
            fuel1_azs_value = fuel1_azs.value if fuel1_azs.value else "Не выбрана"

            octane_2 = float(fuel2_octane.value) if fuel2_octane.value else 0
            volume_2 = float(fuel2_volume.value) if fuel2_volume.value else 0
            fuel2_type_value = fuel2_type.value if fuel2_type.value else "Не выбран"
            fuel2_azs_value = fuel2_azs.value if fuel2_azs.value else "Не выбрана"

            # Проверяем, что есть хоть какое-то топливо
            if not tank_checkbox.value and volume_1 == 0 and volume_2 == 0:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Добавьте объем топлива хотя бы в одну заправку!"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()
                return

            # Рассчитываем общий объем
            total_volume = volume_tank + volume_1 + volume_2

            if total_volume > 0:
                # Рассчитываем среднее октановое число
                total_octane = (octane_tank * volume_tank +
                                octane_1 * volume_1 +
                                octane_2 * volume_2)
                avg_octane = total_octane / total_volume

                # Выводим результат
                result_octane.value = f"{avg_octane:.1f}"
                result_volume.value = f"{total_volume:.1f}"

                # Сохраняем в историю
                history_record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "fuels": {
                        "tank": {
                            "azs": fuel_tank_azs,
                            "type": fuel_tank_type,
                            "octane": octane_tank,
                            "volume": volume_tank
                        },
                        "fuel1": {
                            "azs": fuel1_azs_value,
                            "type": fuel1_type_value,
                            "octane": octane_1,
                            "volume": volume_1
                        },
                        "fuel2": {
                            "azs": fuel2_azs_value,
                            "type": fuel2_type_value,
                            "octane": octane_2,
                            "volume": volume_2
                        }
                    },
                    "result": {
                        "octane": f"{avg_octane:.1f}",
                        "volume": f"{total_volume:.1f}"
                    }
                }

                if add_history_record(history_record):
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Расчет выполнен успешно! История сохранена."),
                        bgcolor=ft.Colors.GREEN,
                    )
                else:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Расчет выполнен, но история не сохранена!"),
                        bgcolor=ft.Colors.ORANGE,
                    )

                # ✅ ПОКАЗЫВАЕМ РЕКЛАМУ ПОСЛЕ УСПЕШНОГО РАСЧЕТА
                if hasattr(page, 'open_ad_in_browser'):
                    async def show_ad_after_calc():
                        await asyncio.sleep(0.5)  # Небольшая задержка
                        page.open_ad_in_browser()
                    page.run_task(show_ad_after_calc)
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Добавьте объем топлива!"),
                    bgcolor=ft.Colors.RED,
                )

            page.snack_bar.open = True
            page.update()

        except ValueError:
            page.snack_bar = ft.SnackBar(
                ft.Text("Введите корректные числовые значения!"),
                bgcolor=ft.Colors.RED,
            )
            page.snack_bar.open = True
            page.update()

    def clear_fields(e):
        """Очищает все поля"""
        tank_checkbox.value = False
        tank_container.visible = False
        tank_azs.value = None
        tank_fuel_type.value = None
        tank_fuel_type.options = []
        tank_octane.value = ""
        tank_volume.value = ""

        fuel1_azs.value = None
        fuel1_type.value = None
        fuel1_type.options = []
        fuel1_octane.value = ""
        fuel1_volume.value = ""

        fuel2_azs.value = None
        fuel2_type.value = None
        fuel2_type.options = []
        fuel2_octane.value = ""
        fuel2_volume.value = ""

        result_octane.value = ""
        result_volume.value = ""

        page.update()

    return constrain_width(page, ft.Container(
        expand=True,
        padding=12,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                # Логотип и название
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                    controls=[
                        ft.Image(
                            src="logo.png",
                            width=30,
                            height=30,
                        ),
                        ft.Text(
                            "Fuel",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Mix",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN,
                        ),
                    ],
                ),

                # Топливо в баке с чекбоксом
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Text(
                            "Топливо в баке",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                        ),
                        tank_checkbox,
                    ],
                ),

                # Контейнер с полями для топлива в баке (скрыт по умолчанию)
                tank_container,

                ft.Divider(height=1),

                # Топливо для заправки №1
                ft.Text(
                    "Топливо для заправки №1",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                ),
                fuel1_column,

                ft.Divider(height=1),

                # Топливо для заправки №2
                ft.Text(
                    "Топливо для заправки №2",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                ),
                fuel2_column,

                ft.Divider(height=1),

                # Результат
                ft.Text(
                    "Результат смешивания",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    controls=[
                        result_octane,
                        result_volume,
                    ],
                    spacing=10,
                ),

                # Кнопки
                ft.Row(
                    controls=[
                        ft.FilledButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.CALCULATE),
                                    ft.Text("Рассчитать"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            on_click=calculate_mixture,
                            expand=True,
                            height=50,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=18),
                            ),
                        ),
                        ft.OutlinedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.CLEAR),
                                    ft.Text("Очистить"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            on_click=clear_fields,
                            expand=True,
                            height=50,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=18),
                            ),
                        ),
                    ],
                    spacing=10,
                ),
            ],
        ),
    ))