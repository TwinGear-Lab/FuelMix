import flet as ft
import flet_webview as ftwv


def view(page: ft.Page):

    return ftwv.WebView(
        url="https://toplivo.tbank.ru/?utm_source=autoru&utm_medium=bz_post",
        expand=True,
    )