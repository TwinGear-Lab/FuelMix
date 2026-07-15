import flet as ft
import json
import os

# Путь к файлу с данными (корень проекта)
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataAGS.json")


def load_data():
    """Загружает данные из JSON файла"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return {}


def save_data(data):
    """Сохраняет данные в JSON файл"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")
        return False


def view(page: ft.Page):
    print("Загрузка страницы настроек АЗС")

    # Загружаем данные
    data = load_data()

    # Получаем список АЗС
    gas_stations_rf = list(data.keys())
    print(f"Найдено АЗС: {gas_stations_rf}")

    # Контейнер для отображения выбранной АЗС
    selected_station_container = ft.Container()

    # Выпадающий список для выбора АЗС
    station_dropdown = ft.Dropdown(
        width=350,
        label="Выберите АЗС",
        hint_text="Выберите АЗС из списка",
        options=[
            ft.dropdown.Option(station) for station in gas_stations_rf
        ],
    )

    # Если есть АЗС, выбираем первую по умолчанию
    if gas_stations_rf:
        station_dropdown.value = gas_stations_rf[0]

    def load_station_data(e):
        """Загружает данные выбранной АЗС (по нажатию кнопки)"""
        station_name = station_dropdown.value
        print(f"Загрузка данных для АЗС: {station_name}")

        if not station_name:
            page.snack_bar = ft.SnackBar(
                ft.Text("Выберите АЗС из списка!"),
                bgcolor=ft.Colors.RED,
            )
            page.snack_bar.open = True
            page.update()
            return

        data = load_data()
        fuels = data.get(station_name, {})

        # Создаем карточку с информацией о АЗС
        station_card = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=12,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                station_name,
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                tooltip="Удалить АЗС",
                                on_click=lambda e: delete_station(station_name),
                            ),
                        ]
                    ),
                    ft.Divider(height=10),
                    # Список топлива
                    ft.Text(
                        "Топливо на заправке:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Column(
                        controls=[
                            create_fuel_row(station_name, fuel_name, octane)
                            for fuel_name, octane in fuels.items()
                        ],
                        spacing=8,
                    ),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.ADD,
                                icon_color=ft.Colors.GREEN,
                                tooltip="Добавить топливо",
                                on_click=lambda e: show_add_fuel_dialog(station_name),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                spacing=10,
            ),
        )

        selected_station_container.content = station_card
        page.update()

    def create_fuel_row(station_name, fuel_name, octane):
        """Создает строку с информацией о топливе"""
        fuel_octane_field = ft.TextField(
            value=str(octane),
            width=80,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
            dense=True,
        )

        def save_fuel_change(e):
            try:
                new_octane = float(fuel_octane_field.value)
                print(f"Сохранение: {station_name} -> {fuel_name} = {new_octane}")
                data = load_data()
                if station_name in data and fuel_name in data[station_name]:
                    data[station_name][fuel_name] = new_octane
                    if save_data(data):
                        page.snack_bar = ft.SnackBar(
                            ft.Text(f"Октановое число обновлено: {fuel_name} = {new_octane}"),
                            bgcolor=ft.Colors.GREEN,
                        )
                        page.snack_bar.open = True
                        page.update()
            except ValueError:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Введите корректное число!"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()

        def delete_fuel(e):
            print(f"Удаление топлива: {station_name} -> {fuel_name}")
            data = load_data()
            if station_name in data and fuel_name in data[station_name]:
                del data[station_name][fuel_name]
                if save_data(data):
                    update_dropdown()
                    load_station_data(None)
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"Топливо {fuel_name} удалено"),
                        bgcolor=ft.Colors.ORANGE,
                    )
                    page.snack_bar.open = True
                    page.update()

        return ft.Container(
            padding=5,
            content=ft.Row(
                controls=[
                    ft.Text(fuel_name, expand=True, size=15, weight=ft.FontWeight.W_500),
                    fuel_octane_field,
                    ft.Text("ОЧ", size=13),
                    ft.IconButton(
                        icon=ft.Icons.SAVE,
                        icon_size=20,
                        icon_color=ft.Colors.GREEN,
                        tooltip="Сохранить",
                        on_click=save_fuel_change,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_size=20,
                        icon_color=ft.Colors.RED,
                        tooltip="Удалить топливо",
                        on_click=delete_fuel,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

    def delete_station(station_name):
        """Удаляет АЗС"""
        print(f"Удаление АЗС: {station_name}")

        def confirm_delete(e):
            print(f"Подтверждено удаление: {station_name}")
            data = load_data()
            if station_name in data:
                del data[station_name]
                if save_data(data):
                    update_dropdown()
                    new_data = load_data()
                    if new_data:
                        first_station = list(new_data.keys())[0]
                        station_dropdown.value = first_station
                        load_station_data(None)
                    else:
                        station_dropdown.value = None
                        selected_station_container.content = ft.Text("Нет доступных АЗС для редактирования")

                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"АЗС {station_name} удалена"),
                        bgcolor=ft.Colors.ORANGE,
                    )
                    page.snack_bar.open = True
                    page.update()
            page.dialog.open = False
            page.update()

        def cancel_delete(e):
            print("Отмена удаления")
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Подтверждение удаления"),
            content=ft.Text(f"Вы уверены, что хотите удалить АЗС '{station_name}' и все ее топливо?"),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_delete),
                ft.TextButton("Удалить", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    def update_dropdown():
        """Обновляет выпадающий список"""
        data = load_data()
        stations = list(data.keys())
        station_dropdown.options = [ft.dropdown.Option(station) for station in stations]
        page.update()

    def show_add_station_dialog(e):
        """Показывает диалог добавления новой АЗС"""
        print("Открытие диалога добавления АЗС")
        station_name_field = ft.TextField(
            label="Название АЗС",
            hint_text="Введите название АЗС",
            width=300,
        )

        def add_station(e):
            name = station_name_field.value.strip()
            print(f"Добавление АЗС: {name}")

            if not name:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Введите название АЗС!"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()
                return

            data = load_data()
            if name in data:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Такая АЗС уже существует!"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()
                return

            data[name] = {}
            if save_data(data):
                page.dialog.open = False
                update_dropdown()
                station_dropdown.value = name
                load_station_data(None)
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"АЗС '{name}' добавлена!"),
                    bgcolor=ft.Colors.GREEN,
                )
                page.snack_bar.open = True
                page.update()

        def cancel_add(e):
            print("Отмена добавления АЗС")
            page.dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Добавить новую АЗС"),
            content=station_name_field,
            actions=[
                ft.TextButton("Отмена", on_click=cancel_add),
                ft.FilledButton("Добавить", on_click=add_station),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def show_add_fuel_dialog(station_name):
        """Показывает диалог добавления нового топлива"""
        print(f"Открытие диалога добавления топлива для: {station_name}")
        fuel_name_field = ft.TextField(
            label="Название топлива",
            hint_text="Например: АИ-95",
            width=250,
        )
        fuel_octane_field = ft.TextField(
            label="Октановое число",
            hint_text="Например: 95",
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
            width=150,
        )

        def add_fuel(e):
            fuel_name = fuel_name_field.value.strip()
            octane_str = fuel_octane_field.value.strip()

            print(f"Добавление топлива: {fuel_name} = {octane_str} для {station_name}")

            if not fuel_name:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Введите название топлива!"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()
                return

            if not octane_str:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Введите октановое число!"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()
                return

            try:
                octane = float(octane_str)
                data = load_data()

                if station_name not in data:
                    data[station_name] = {}

                if fuel_name in data[station_name]:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Такое топливо уже существует!"),
                        bgcolor=ft.Colors.RED,
                    )
                    page.snack_bar.open = True
                    page.update()
                    return

                data[station_name][fuel_name] = octane
                if save_data(data):
                    page.dialog.open = False
                    update_dropdown()
                    load_station_data(None)
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"Топливо '{fuel_name}' добавлено!"),
                        bgcolor=ft.Colors.GREEN,
                    )
                    page.snack_bar.open = True
                    page.update()

            except ValueError:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Введите корректное число!"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()

        def cancel_add(e):
            print("Отмена добавления топлива")
            page.dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(f"Добавить топливо для {station_name}"),
            content=ft.Column(
                controls=[
                    fuel_name_field,
                    fuel_octane_field,
                ],
                spacing=10,
                width=400,
            ),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_add),
                ft.FilledButton("Добавить", on_click=add_fuel),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    # Создаем страницу
    result = ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Настройки АЗС",
                            size=30,
                            weight="bold",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            icon_size=30,
                            tooltip="Добавить АЗС",
                            on_click=show_add_station_dialog,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text(
                    "Выберите АЗС из списка и нажмите 'Загрузить' для редактирования",
                    size=16,
                ),
                ft.Divider(height=10),
                # Выпадающий список и кнопка загрузки
                ft.Row(
                    controls=[
                        station_dropdown,
                        ft.FilledButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.FILE_OPEN),
                                    ft.Text("Загрузить"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            on_click=load_station_data,
                            width=150,
                            height=45,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Divider(height=20),
                # Контейнер для выбранной АЗС
                selected_station_container,
            ],
        ),
    )

    # Загружаем первую АЗС если есть
    if gas_stations_rf:
        load_station_data(None)
    else:
        selected_station_container.content = ft.Text("Нет доступных АЗС. Добавьте новую АЗС с помощью кнопки '+'")

    return result