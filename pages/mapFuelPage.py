import flet as ft
import flet_webview as ftwv

from widgets.navigationPanel import navigation_panel


def view(page: ft.Page):
    # Создаём WebView с картой
    webview = ftwv.WebView(
        url="https://yandex.ru/maps/50/perm/search/азс/?ll=56.229441%2C58.010454&sll=56.229441%2C58.010454&sspn=0.326157%2C0.115348&z=12",
        expand=True,
    )
    
    return ft.View(
        "/map",
        bgcolor="#101418",
        navigation_bar=navigation_panel(page, 3),
        controls=[
            # Верхняя панель с заголовком
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,  # 👈 правильно ARROW_BACK, без знака подчёркивания
                        on_click=lambda e: page.go("/"),
                        icon_color="#FFFFFF",
                    ),
                    ft.Text(
                        "Карта АЗС",
                        size=24,
                        weight="bold",
                        color="#FFFFFF",
                    ),
                ],
                alignment="start",
            ),
            # Контейнер с WebView
            ft.Container(
                content=webview,
                expand=True,
                border_radius=12,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
        ],
    )