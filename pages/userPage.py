import flet as ft
from theme import get_theme_name, get_theme_colors, constrain_width

GREEN = ft.Colors.GREEN
BLUE = ft.Colors.BLUE

setMessage = "Включены"
countChange = 0
countLiters = 0
countRON = 0


def view(page: ft.Page):
    # Получаем цвета для текущей темы
    colors = get_theme_colors()

    # Создаем изменяемые тексты
    notification_text = ft.Text(
        setMessage,
        size=12,
    )
    theme_text = ft.Text(
        get_theme_name(),
        size=12,
    )

    # Для статистики создаем отдельные Text объекты
    changes_display = ft.Text(
        str(countChange),
        size=22,
        weight="bold",
    )

    liters_display = ft.Text(
        str(countLiters),
        size=22,
        weight="bold",
    )

    ron_display = ft.Text(
        str(countRON),
        size=22,
        weight="bold",
    )

    def messageChange(e):
        global setMessage
        if setMessage == "Включены":
            setMessage = "Отключены"
        else:
            setMessage = "Включены"
        notification_text.value = setMessage
        page.update()
        print(f"Уведомления теперь: {setMessage}")

    def on_stations_click(e):
        page.snack_bar = ft.SnackBar(
            ft.Text("Статистика обновлена!"),
            bgcolor=GREEN,
        )
        page.snack_bar.open = True
        page.update()

    def on_theme_click(e):
        print("Нажата тема")

        # Меняем тему через главную страницу
        if hasattr(page, 'change_theme'):
            page.change_theme()

        # Обновляем текст темы
        theme_text.value = get_theme_name()
        page.update()

        page.snack_bar = ft.SnackBar(
            ft.Text(f"Тема изменена на {theme_text.value}"),
            bgcolor=GREEN,
        )
        page.snack_bar.open = True
        page.update()

    def reset_values(e):
        global countChange, countLiters, countRON

        countChange = 0
        countLiters = 0
        countRON = 0

        changes_display.value = str(countChange)
        liters_display.value = str(countLiters)
        ron_display.value = str(countRON)

        page.snack_bar = ft.SnackBar(
            ft.Text("Все значения обнулены!"),
            bgcolor=GREEN,
        )
        page.snack_bar.open = True
        page.update()
        print("Значения обнулены")

    # Создаем аватар (только стандартная иконка)
    avatar = ft.Container(
        bgcolor=GREEN,
        width=100,
        height=100,
        border_radius=50,
        content=ft.Icon(
            ft.Icons.PERSON,
            size=50,
            color=ft.Colors.WHITE,
        )
    )

    # Создаем кнопки настроек
    notification_item = ft.Container(
        padding=15,
        on_click=messageChange,
        ink=True,
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.NOTIFICATIONS,
                    color=BLUE,
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Text(
                            "Уведомления",
                            size=16,
                        ),
                        notification_text,
                    ],
                ),
                ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS,
                    size=16,
                )
            ],
        ),
    )

    stations_item = ft.Container(
        padding=15,
        on_click=on_stations_click,
        ink=True,
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.LOCAL_GAS_STATION,
                    color=BLUE,
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Text(
                            "Избранные АЗС",
                            size=16,
                        ),
                        ft.Text(
                            "Лукойл",
                            size=12,
                        ),
                    ],
                ),
                ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS,
                    size=16,
                )
            ],
        ),
    )

    theme_item = ft.Container(
        padding=15,
        on_click=on_theme_click,
        ink=True,
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.DARK_MODE,
                    color=BLUE,
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Text(
                            "Тема",
                            size=16,
                        ),
                        theme_text,
                    ],
                ),
                ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS,
                    size=16,
                )
            ],
        ),
    )

    return constrain_width(ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15,
            controls=[
                # Заголовок
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Профиль",
                            size=30,
                            weight="bold",
                        ),
                    ],
                ),

                # Карточка пользователя
                ft.Container(
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    border_radius=15,
                    padding=20,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            avatar,
                            ft.Container(height=10),
                            ft.Text(
                                "Водитель",
                                size=22,
                                weight="bold",
                            ),
                            ft.Text(
                                "Пользователь FuelMix",
                            ),
                        ],
                    ),
                ),

                # Статистика
                ft.Text(
                    "Статистика",
                    size=20,
                    weight="bold",
                ),

                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            expand=True,
                            bgcolor=ft.Colors.SURFACE_CONTAINER,
                            border_radius=12,
                            padding=15,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.SYNC,
                                        color=GREEN,
                                    ),
                                    changes_display,
                                    ft.Text(
                                        "Смешиваний",
                                        size=12,
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            bgcolor=ft.Colors.SURFACE_CONTAINER,
                            border_radius=12,
                            padding=15,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.LOCAL_GAS_STATION,
                                        color=GREEN,
                                    ),
                                    liters_display,
                                    ft.Text(
                                        "Литров",
                                        size=12,
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            bgcolor=ft.Colors.SURFACE_CONTAINER,
                            border_radius=12,
                            padding=15,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.SPEED,
                                        color=GREEN,
                                    ),
                                    ron_display,
                                    ft.Text(
                                        "Средний RON",
                                        size=12,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),

                # Настройки
                ft.Text(
                    "Настройки",
                    size=20,
                    weight="bold",
                ),

                ft.Container(
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            notification_item,
                            stations_item,
                            theme_item,
                        ]
                    ),
                ),

                # Кнопка выхода
                ft.FilledButton(
                    "Обнулить значения",
                    icon=ft.Icons.RESTORE,
                    on_click=reset_values,
                    expand=True,
                ),
            ],
        ),
    ))