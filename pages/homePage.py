import flet as ft

def view(page: ft.Page):
    gas_stations_rf = [
        "Лукойл", "Роснефть", "Газпромнефть", "Газпром", "Татнефть",
        "Башнефть", "Teboil", "Shell", "Нефтьмагистраль", "Трасса",
        "IRBIS", "TNK BP", "ННК", "Сургутнефтегаз", "Русойл",
        "Славнефть", "Сибнефть"
    ]

    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
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

                ft.Text(
                    "Топливо в баке",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Dropdown(
                            width=200,
                            label="АЗС",
                            hint_text="Выберите АЗС",
                            options=[
                                ft.dropdown.Option(station)
                                for station in gas_stations_rf
                            ],
                        ),
                        ft.Dropdown(
                            width=180,
                            label="Тип топлива",
                            hint_text="Выберите топливо",
                            options=[
                                ft.dropdown.Option("АИ-92"),
                                ft.dropdown.Option("АИ-95"),
                                ft.dropdown.Option("АИ-98"),
                                ft.dropdown.Option("АИ-100"),
                            ],
                        ),
                    ],
                ),

                ft.TextField(
                    width=200,
                    hint_text="Объем топлива",
                    suffix=ft.Text("л"),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    input_filter=ft.NumbersOnlyInputFilter(),
                    filled=True,
                ),
            ],
        ),
    )