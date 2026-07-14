import flet as ft
import flet_webview as ftwv

def main(page: ft.Page):

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                label="Главная",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.MAP,
                label="Карта",
            ),
        ]
    )

    page.add(
        ft.Container(
            expand=True,
            content=ftwv.WebView(
                url="https://example.com",
                expand=True,
            ),
        )
    )

ft.run(main)
