import flet as ft

#топливо в баке
#выбранная заправка
str_selectAGS_Tank = ft.TextField()
#тип топлива
str_typeFuelTank = ft.TextField()
#объем топлива
num_volumeFuel = ft.TextField()

#топливо для заправки 1
#выбранная заправка
str_selectAGS_One = ft.TextField()
#тип топлива
str_typeFuelOne = ft.TextField()
#объем топлива
num_volumeOne = ft.TextField()

#топливо для заправки 2
#выбранная заправка
str_selectAGS_Two = ft.TextField()
#тип топлива
str_typeFuelTwo = ft.TextField()
#объем топлива
num_volumeTwo = ft.TextField()

#результат топлива
#октановое число
num_resultOctan = ft.TextField()
#литры
num_resultFuel = ft.TextField()

def view(page: ft.Page):
    gas_stations_rf = [
        "Лукойл", "Роснефть", "Газпромнефть", "Газпром", "Татнефть",
        "Башнефть", "Teboil", "Shell", "Нефтьмагистраль", "Трасса",
        "IRBIS", "TNK BP", "ННК", "Сургутнефтегаз", "Русойл",
        "Славнефть", "Сибнефть"
    ]

    return ft.Container(

        expand=True,
        padding=0,
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
                            color=ft.Colors.WHITE,
                        ),
                        ft.Text(
                            "Mix",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN,
                        ),
                    ],
                ),


                #топливо котрое находитсе уже в баке
                ft.Text(
                    "Топливо в баке",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
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

                # топливо которым будем заправляться 1
                ft.Text(
                    "Топливо для заправки №1",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
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

                # топливо которым будем заправляться 2
                ft.Text(
                    "Топливо для заправки №2",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
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

                # результат смешивания
                ft.Text(
                    "Результат октанового числа",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),

                ft.TextField(
                    width=200,
                    hint_text="Октановое число",
                    suffix=ft.Text("ОЧ"),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    input_filter=ft.NumbersOnlyInputFilter(),
                    filled=True,
                ),

                ft.TextField(
                    width=200,
                    hint_text="Объем топлива",
                    suffix=ft.Text("л"),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    input_filter=ft.NumbersOnlyInputFilter(),
                    filled=True,
                ),

                ft.FilledButton(
                    content=ft.Text("Рассчитать смесь"),
                    width=300,
                    height=55,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=18),
                    ),
                ),
            ],
        ),
    )