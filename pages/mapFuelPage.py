import flet as ft
import flet_webview as ftwv


def view(page: ft.Page):

    return ftwv.WebView(
        #https://gdebenz.ru/
        url="https://yandex.ru/maps/50/perm/search/азс/?ll=56.229441%2C58.010454&sll=56.229441%2C58.010454&sspn=0.310020%2C0.110610&z=12",
        expand=True,
    )