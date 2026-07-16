import flet as ft
import flet_webview as ftwv


def view(page: ft.Page):

    return ftwv.WebView(
        url="https://gdebenz.ru/",
        expand=True,
    )