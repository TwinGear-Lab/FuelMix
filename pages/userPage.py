import flet as ft
from theme import get_theme_name, get_theme_colors, constrain_width
from history_storage import load_history

GREEN = ft.Colors.GREEN
BLUE = ft.Colors.BLUE


def view(page: ft.Page):
    # Получаем цвета для текущей темы
    colors = get_theme_colors()

    # Загружаем историю и вычисляем статистику
    history = load_history()
    total_calculations = len(history)
    total_volume = 0.0
    total_octane_sum = 0.0

    for record in history:
        result = record.get("result", {})
        try:
            octane = float(result.get("octane", 0))
            volume = float(result.get("volume", 0))
            total_octane_sum += octane
            total_volume += volume
        except (ValueError, TypeError):
            pass

    avg_octane = total_octane_sum / total_calculations if total_calculations > 0 else 0

    # Создаем изменяемые тексты
    notification_text = ft.Text(
        "Включены",
        size=12,
    )
    theme_text = ft.Text(
        get_theme_name(),
        size=12,
    )

    # Для статистики создаем отдельные Text объекты
    changes_display = ft.Text(
        str(total_calculations),
        size=22,
        weight="bold",
    )

    liters_display = ft.Text(
        f"{total_volume:.1f}",
        size=22,
        weight="bold",
    )

    ron_display = ft.Text(
        f"{avg_octane:.1f}",
        size=22,
        weight="bold",
    )

    def messageChange(e):
        if notification_text.value == "Включены":
            notification_text.value = "Отключены"
        else:
            notification_text.value = "Включены"
        page.update()
        print(f"Уведомления теперь: {notification_text.value}")

    def on_stations_click(e):
        page.snack_bar = ft.SnackBar(
            ft.Text("Избранные АЗС"),
            bgcolor=GREEN,
        )
        page.snack_bar.open = True
        page.update()

    def on_theme_click(e):
        print("Нажата тема")

        if hasattr(page, 'change_theme'):
            page.change_theme()

        theme_text.value = get_theme_name()
        page.update()

        page.snack_bar = ft.SnackBar(
            ft.Text(f"Тема изменена на {theme_text.value}"),
            bgcolor=GREEN,
        )
        page.snack_bar.open = True
        page.update()

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

    return constrain_width(page, ft.Container(
        expand=True,
        padding=12,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                    padding=10,
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
                            padding=10,
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
                                        size=10,
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            bgcolor=ft.Colors.SURFACE_CONTAINER,
                            border_radius=12,
                            padding=10,
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
                                        size=10,
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            bgcolor=ft.Colors.SURFACE_CONTAINER,
                            border_radius=12,
                            padding=10,
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
                                        size=10,
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
                    border_radius=10,
                    content=ft.Column(
                        controls=[
                            notification_item,
                            stations_item,
                            theme_item,
                        ]
                    ),
                ),
            ],
        ),
    ))