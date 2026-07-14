import flet as ft


def view(page: ft.Page):

    return ft.Container(
        padding=10,
        content=ft.Row(
            spacing=0,
            controls=[
                ft.Text(
                    "Fuel",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    "Mix",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN,
                ),
            ],
        ),
    )
