import flet as ft


BG = "#101418"
CARD = "#1A1F24"
GREEN = "#5CC85C"
BLUE = "#4B8DFF"
TEXT = "#FFFFFF"
TEXT2 = "#9EA6AF"


def view(page: ft.Page):

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,

        controls=[

            # Заголовок
            ft.Text(
                "Профиль",
                size=30,
                weight="bold",
                color=TEXT,
            ),


            # Карточка пользователя
            ft.Container(
                bgcolor=CARD,
                border_radius=15,
                padding=20,

                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.CircleAvatar(
                            radius=45,
                            bgcolor=GREEN,
                            content=ft.Icon(
                                ft.Icons.PERSON,
                                size=50,
                                color=BG,
                            ),
                        ),

                        ft.Container(height=10),

                        ft.Text(
                            "Водитель",
                            size=22,
                            weight="bold",
                            color=TEXT,
                        ),

                        ft.Text(
                            "Пользователь FuelMix",
                            color=TEXT2,
                        ),

                    ],
                ),
            ),


            # Статистика
            ft.Text(
                "Статистика",
                size=20,
                weight="bold",
                color=TEXT,
            ),


            ft.Row(
                spacing=10,

                controls=[

                    statistic_card(
                        "Смешиваний",
                        "25",
                        ft.Icons.SYNC,
                    ),

                    statistic_card(
                        "Литров",
                        "540",
                        ft.Icons.LOCAL_GAS_STATION,
                    ),

                    statistic_card(
                        "Средний RON",
                        "95.3",
                        ft.Icons.SPEED,
                    ),

                ],
            ),


            # Настройки
            ft.Text(
                "Настройки",
                size=20,
                weight="bold",
                color=TEXT,
            ),


            ft.Container(
                bgcolor=CARD,
                border_radius=15,

                content=ft.Column(
                    controls=[

                        profile_item(
                            ft.Icons.NOTIFICATIONS,
                            "Уведомления",
                            "Включены",
                        ),

                        profile_item(
                            ft.Icons.LOCAL_GAS_STATION,
                            "Избранные АЗС",
                            "Лукойл",
                        ),

                        profile_item(
                            ft.Icons.SCALE,
                            "Единицы измерения",
                            "Литры",
                        ),

                        profile_item(
                            ft.Icons.DARK_MODE,
                            "Тема",
                            "Тёмная",
                        ),

                    ]
                ),
            ),


            # Кнопка выхода
            ft.FilledButton(
                "Выйти из профиля",
                icon=ft.Icons.LOGOUT,
            )

        ],
    )



def statistic_card(title, value, icon):

    return ft.Container(

        expand=True,

        bgcolor=CARD,
        border_radius=12,
        padding=15,

        content=ft.Column(

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Icon(
                    icon,
                    color=GREEN,
                ),

                ft.Text(
                    value,
                    size=22,
                    weight="bold",
                    color=TEXT,
                ),

                ft.Text(
                    title,
                    size=12,
                    color=TEXT2,
                ),

            ],
        ),
    )



def profile_item(icon, title, subtitle):

    return ft.Container(

        padding=15,

        content=ft.Row(

            controls=[

                ft.Icon(
                    icon,
                    color=BLUE,
                ),

                ft.Column(
                    expand=True,

                    controls=[

                        ft.Text(
                            title,
                            color=TEXT,
                            size=16,
                        ),

                        ft.Text(
                            subtitle,
                            color=TEXT2,
                            size=12,
                        ),

                    ],
                ),

                ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS,
                    size=16,
                    color=TEXT2,
                )

            ],
        ),
    )