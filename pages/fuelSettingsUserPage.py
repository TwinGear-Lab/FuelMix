import flet as ft

from widgets.navigationPanel import navigation_panel

def view(page: ft.Page):

    return ft.View(
        route="/settings",
        navigation_bar=navigation_panel(page, 2),
        controls=[
            ft.Text(
                "Настройки АЗС",
                size=30,
                weight="bold",
            ),
        ],
    )