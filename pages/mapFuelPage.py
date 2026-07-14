import flet as ft
import flet_webview as ftwv


def view(page: ft.Page):

    return ftwv.WebView(
        url="https://yandex.ru/maps/50/perm/search/азс/?ll=56.206985%2C57.997407&sll=56.229441%2C58.010454&sspn=0.326157%2C0.131748&z=12",
        expand=True,
    )