import flet as ft


def view(page: ft.Page):
    # Настройка страницы для центрирования
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    async def open_map(e):
        await page.launch_url("https://gdebenz.ru/perm")

    return ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Icon(
                    ft.Icons.LOCAL_GAS_STATION,
                    size=100,
                    color=ft.Colors.BLUE_400,
                ),
                ft.Text(
                    "Карта АЗС",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Нажмите кнопку,\nчтобы открыть карту с ближайшими АЗС.",
                    text_align=ft.TextAlign.CENTER,
                    size=16,
                    color=ft.Colors.GREY_600,
                ),
                ft.ElevatedButton(
                    "Открыть карту",
                    icon=ft.Icons.MAP,
                    on_click=open_map,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=20,  # Просто число - работает для всех сторон
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )