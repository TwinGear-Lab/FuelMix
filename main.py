import flet as ft
from pages import fuelSettingsUserPage
from pages import historyPage
from pages import homePage
from pages import mapFuelPage
from pages import userPage

# -----------------------------
# Цветовая схема
# -----------------------------
BG = "#101418"
CARD = "#1A1F24"
GREEN = "#5CC85C"
BLUE = "#4B8DFF"
TEXT = "#FFFFFF"
TEXT2 = "#9EA6AF"


# -----------------------------
# Виджет карточки топлива
# -----------------------------
def fuel_card(title, station, fuel, ron, color):
    return ft.Container(
        bgcolor=CARD,
        border_radius=12,
        padding=15,
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Text(title, size=16, weight="bold", color=color),

                ft.Row(
                    controls=[
                        ft.Dropdown(
                            label="АЗС",
                            value=station,
                            options=[
                                ft.dropdown.Option("Лукойл"),
                                ft.dropdown.Option("Газпромнефть"),
                                ft.dropdown.Option("Роснефть"),
                            ],
                            expand=True,
                        ),

                        ft.Dropdown(
                            label="Марка топлива",
                            value=fuel,
                            options=[
                                ft.dropdown.Option("АИ-92"),
                                ft.dropdown.Option("АИ-95"),
                                ft.dropdown.Option("АИ-100"),
                            ],
                            expand=True,
                        ),
                    ]
                ),

                ft.TextField(
                    label="Октановое число",
                    value=ron,
                ),

                ft.TextField(
                    label="Количество (л)",
                    value="17.5",
                ),

                ft.Slider(
                    min=0,
                    max=100,
                    value=17.5,
                    active_color=color,
                )
            ],
        ),
    )


# -----------------------------
# Карточка результата
# -----------------------------
def result_card():
    return ft.Container(
        bgcolor=CARD,
        border_radius=12,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Результат смешивания",
                    color=GREEN,
                    weight="bold",
                    size=18,
                ),

                ft.Text(
                    "95.0",
                    size=46,
                    weight="bold",
                    color=GREEN,
                ),

                ft.Container(
                    bgcolor="#17361E",
                    border_radius=8,
                    padding=10,
                    content=ft.Text(
                        "Соответствует АИ-95",
                        color=GREEN,
                    ),
                ),

                ft.Row(
                    alignment="spaceAround",
                    controls=[
                        info_item("Объем", "27.7 л"),
                        info_item("Цена", "54.12 ₽"),
                        info_item("Стоимость", "1499 ₽"),
                    ],
                ),

                ft.Row(
                    controls=[
                        ft.FilledButton(
                            "Сохранить",
                            expand=True,
                        ),
                        ft.OutlinedButton(
                            "Поделиться",
                            expand=True,
                        ),
                    ]
                )
            ]
        )
    )


def info_item(title, value):
    return ft.Column(
        horizontal_alignment="center",
        controls=[
            ft.Text(title, color=TEXT2, size=12),
            ft.Text(value, color=TEXT, weight="bold"),
        ]
    )


# -----------------------------
# Таблица ближайших АЗС
# -----------------------------
def gas_station_list():
    stations = [
        ("Лукойл", "95.2", "1.2 км", "53.80 ₽"),
        ("Газпромнефть", "95.3", "2.1 км", "53.20 ₽"),
        ("Роснефть", "95.6", "2.8 км", "53.50 ₽"),
    ]

    rows = []

    for name, ron, dist, price in stations:
        rows.append(
            ft.Container(
                padding=10,
                border_radius=8,
                bgcolor="#151A20",
                content=ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Text(name),
                        ft.Text(f"RON {ron}", color=GREEN),
                        ft.Text(dist),
                        ft.Text(price),
                    ],
                ),
            )
        )

    return ft.Container(
        bgcolor=CARD,
        border_radius=12,
        padding=15,
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Text(
                            "Ближайшие АЗС",
                            size=18,
                            weight="bold",
                        ),
                        ft.TextButton("Показать на карте"),
                    ],
                ),
                *rows,
            ]
        ),
    )

    # -----------------------------
    # Маршрутизация
    # -----------------------------

    def route_change(e):
        page.views.clear()

        # Главная страница
        if page.route == "/":
            page.views.append(get_main_view())

        # Страница настроек АЗС
        elif page.route == "/settings":
            page.views.append(gas_station_settings_page())

        # Страница истории
        elif page.route == "/history":
            page.views.append(history_page())

        # Страница профиля
        elif page.route == "/profile":
            page.views.append(profile_page())

        # Страница карты
        elif page.route == "/map":
            page.views.append(map_page())

        # Если страница не найдена
        else:
            page.views.append(
                ft.View(
                    "/error",
                    bgcolor=BG,
                    controls=[
                        ft.Text("Страница не найдена", color=TEXT, size=24),
                        ft.ElevatedButton("На главную", on_click=lambda e: page.go("/")),
                    ],
                )
            )

        page.update()

# -----------------------------
# Главное окно
# -----------------------------
def main(page: ft.Page):

    #название окна приложения
    page.title = "FuelMix"

    #page.theme_mode = ft.ThemeMode.DARK

    page.bgcolor = BG # цвет фона

    page.padding = 15 # отступ

    page.scroll = ft.ScrollMode.AUTO

    # нижняя навигация приложения
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                label="Главная",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.HISTORY,
                label="История",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.LOCAL_GAS_STATION,
                label="Настройки АЗС",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.MAP,
                label="АЗС",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON,
                label="Профиль",
            ),
        ]
    )

   #отрисовка окна приложения
    page.add(

        ft.Text(
            "FuelMix",
            size=28,
            weight="bold",
        ),

        ft.Text(
            "Калькулятор октанового числа",
            color=TEXT2,
        ),

        fuel_card(
            "Топливо в баке",
            "Лукойл",
            "АИ-95",
            "95.2",
            GREEN,
        ),

        fuel_card(
            "Топливо на заправке",
            "Газпромнефть",
            "АИ-100",
            "100.6",
            BLUE,
        ),

        result_card(),

        gas_station_list(),
    )


ft.app(target=main)