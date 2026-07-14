import flet as ft


def view(page: ft.Page):

    return ft.Column(
        controls=[

            ft.Text(
                "История",
                size=30,
                weight="bold",
            ),


            ft.Container(
                bgcolor="#1A1F24",
                border_radius=12,
                padding=15,

                content=ft.Column(
                    controls=[

                        ft.Text(
                            "АИ-92 + АИ-100"
                        ),

                        ft.Text(
                            "Получено: АИ-95.0"
                        ),

                        ft.Text(
                            "27.7 литров"
                        ),

                    ]
                )
            )

        ]
    )