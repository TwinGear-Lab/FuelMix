import flet as ft

def view(page: ft.Page):
    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Настройки АЗС",
                    size=30,
                    weight="bold",
                ),
                ft.Text(
                    "Здесь будут настройки ваших АЗС",
                    size=16,
                ),
            ]
        ),
    )