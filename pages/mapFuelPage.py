import flet as ft
import flet_webview as ftwv


def view(page: ft.Page):

    return ftwv.WebView(
        #https://gdebenz.ru/
        url="https://www.google.com/maps/search/АЗС/@58.010454,56.229441,12z",
        expand=True,
    )