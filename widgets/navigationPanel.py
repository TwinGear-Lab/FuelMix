import flet as ft


def navigation_panel(page: ft.Page, selected_index):

    def change(e):

        page.change_page(
            e.control.selected_index
        )


    return ft.NavigationBar(

        selected_index=selected_index,

        on_change=change,

        destinations=[

            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                label="Главная",
            ),

            ft.NavigationBarDestination(
                icon=ft.Icons.HISTORY,
                label="История",
            ),

            ft.NavigationBarDestination(
                icon=ft.Icons.LOCAL_GAS_STATION,
                label="Настройки",
            ),

            ft.NavigationBarDestination(
                icon=ft.Icons.MAP,
                label="АЗС",
            ),

            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON,
                label="Профиль",
            ),

        ]
    )