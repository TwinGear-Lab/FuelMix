import flet as ft
from flet import value
import json



def view(page: ft.Page):

    gas_stations_rf = []


    with open("dataAGS.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        gas_station = list(data.keys())
        for i in range(len(gas_station)):
            gas_stations_rf.append(gas_station[i])

    # Создаем поля ввода с привязкой к переменным
    # Топливо в баке
    tank_azs = ft.Dropdown(
        width=200,
        label="АЗС",
        hint_text="Выберите АЗС",
        options=[ft.dropdown.Option(station) for station in gas_stations_rf],
    )
    tank_fuel_type = ft.Dropdown(
        width=200,
        label="Тип топлива",
        hint_text="Выберите топливо",
        options=[
            ft.dropdown.Option("АИ-92"),
            ft.dropdown.Option("АИ-95"),
            ft.dropdown.Option("АИ-98"),
            ft.dropdown.Option("АИ-100"),
        ],
    )
    tank_octane = ft.TextField(
        width=200,
        hint_text="Октановое число",
        suffix=ft.Text("ОЧ"),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        filled=True,
    )
    tank_volume = ft.TextField(
        width=200,
        hint_text="Объем топлива",
        suffix=ft.Text("л"),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        filled=True,
    )

    # Топливо для заправки №1
    fuel1_azs = ft.Dropdown(
        width=200,
        label="АЗС",
        hint_text="Выберите АЗС",
        options=[ft.dropdown.Option(station) for station in gas_stations_rf],
    )
    fuel1_type = ft.Dropdown(
        width=200,
        label="Тип топлива",
        hint_text="Выберите топливо",
        options=[
            ft.dropdown.Option("АИ-92"),
            ft.dropdown.Option("АИ-95"),
            ft.dropdown.Option("АИ-98"),
            ft.dropdown.Option("АИ-100"),
        ],
    )
    fuel1_octane = ft.TextField(
        width=200,
        hint_text="Октановое число",
        suffix=ft.Text("ОЧ"),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        filled=True,
    )
    fuel1_volume = ft.TextField(
        width=200,
        hint_text="Объем топлива",
        suffix=ft.Text("л"),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        filled=True,
    )

    # Топливо для заправки №2
    fuel2_azs = ft.Dropdown(
        width=200,
        label="АЗС",
        hint_text="Выберите АЗС",
        options=[ft.dropdown.Option(station) for station in gas_stations_rf],
    )
    fuel2_type = ft.Dropdown(
        width=200,
        label="Тип топлива",
        hint_text="Выберите топливо",
        options=[
            ft.dropdown.Option("АИ-92"),
            ft.dropdown.Option("АИ-95"),
            ft.dropdown.Option("АИ-98"),
            ft.dropdown.Option("АИ-100"),
        ],
    )
    fuel2_octane = ft.TextField(
        width=200,
        hint_text="Октановое число",
        suffix=ft.Text("ОЧ"),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        filled=True,
    )
    fuel2_volume = ft.TextField(
        width=200,
        hint_text="Объем топлива",
        suffix=ft.Text("л"),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        filled=True,
    )

    # Результат
    result_octane = ft.TextField(
        width=200,
        hint_text="Октановое число",
        suffix=ft.Text("ОЧ"),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        filled=True,
        read_only=True,
    )
    result_volume = ft.TextField(
        width=200,
        hint_text="Объем топлива",
        suffix=ft.Text("л"),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        filled=True,
        read_only=True,
    )

    def calculate_mixture(e):
        """Рассчитывает смесь топлива"""
        try:
            # Получаем значения
            octane_tank = float(tank_octane.value) if tank_octane.value else 0
            volume_tank = float(tank_volume.value) if tank_volume.value else 0

            octane_1 = float(fuel1_octane.value) if fuel1_octane.value else 0
            volume_1 = float(fuel1_volume.value) if fuel1_volume.value else 0

            octane_2 = float(fuel2_octane.value) if fuel2_octane.value else 0
            volume_2 = float(fuel2_volume.value) if fuel2_volume.value else 0

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

                page.snack_bar = ft.SnackBar(
                    ft.Text("Расчет выполнен успешно!"),
                    bgcolor=ft.Colors.GREEN,
                )
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
        tank_azs.value = None
        tank_fuel_type.value = None
        tank_octane.value = ""
        tank_volume.value = ""

        fuel1_azs.value = None
        fuel1_type.value = None
        fuel1_octane.value = ""
        fuel1_volume.value = ""

        fuel2_azs.value = None
        fuel2_type.value = None
        fuel2_octane.value = ""
        fuel2_volume.value = ""

        result_octane.value = ""
        result_volume.value = ""

        page.update()

    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
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

                # Топливо в баке
                ft.Text(
                    "Топливо в баке",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        tank_azs,
                        tank_fuel_type,
                    ],
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        tank_octane,
                        tank_volume,
                    ],
                ),

                # Разделитель
                ft.Container(height=5),

                # Топливо для заправки №1
                ft.Text(
                    "Топливо для заправки №1",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        fuel1_azs,
                        fuel1_type,
                    ],
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        fuel1_octane,
                        fuel1_volume,
                    ],
                ),

                # Разделитель
                ft.Container(height=5),

                # Топливо для заправки №2
                ft.Text(
                    "Топливо для заправки №2",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        fuel2_azs,
                        fuel2_type,
                    ],
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        fuel2_octane,
                        fuel2_volume,
                    ],
                ),

                # Разделитель
                ft.Container(height=10),

                # Результат
                ft.Text(
                    "Результат смешивания",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        result_octane,
                        result_volume,
                    ],
                ),

                # Кнопки
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.FilledButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.CALCULATE),
                                    ft.Text("Рассчитать смесь"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            on_click=calculate_mixture,
                            width=200,
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
                            width=200,
                            height=50,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=18),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )