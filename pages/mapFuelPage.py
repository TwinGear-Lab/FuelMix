import flet as ft
import flet_webview as ftwv


def view(page: ft.Page):

    return ftwv.WebView(
        #https://gdebenz.ru/
        url="https://m.yandex.ru/maps/50/perm/search/%D0%B0%D0%B7%D1%81/?ll=56.229441%2C58.010454&sll=56.229441%2C58.010454&sspn=0.310020%2C0.110610&z=12",
        expand=True,
    )