import flet as ft

BG = "#101418"
CARD = "#1A1F24"
GREEN = "#5CC85C"
BLUE = "#4B8DFF"
TEXT = "#FFFFFF"
TEXT2 = "#9EA6AF"

setMessage = "Включены"
countChange = 0
countLiters = 0
countRON = 0



def view(page: ft.Page):
    # Создаем изменяемые тексты
    notification_text = ft.Text(
        setMessage,
        color=TEXT2,
        size=12,
    )
    
    # Для статистики создаем отдельные Text объекты
    changes_display = ft.Text(
        str(countChange),
        size=22,
        weight="bold",
        color=TEXT,
    )
    
    liters_display = ft.Text(
        str(countLiters),
        size=22,
        weight="bold",
        color=TEXT,
    )
    
    ron_display = ft.Text(
        str(countRON),
        size=22,
        weight="bold",
        color=TEXT,
    )
    
    """
        def statostics_update(e):
        global countChange, countLiters, countRON
        # Обновляем значения
        countChange += 1
        countLiters += 10
        countRON = 92.5
        
        # Обновляем тексты
        changes_display.value = str(countChange)
        liters_display.value = str(countLiters)
        ron_display.value = str(countRON)
    
        page.update()
    """
    
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
        print(f"Статистика: {countChange}, {countLiters}, {countRON}")
    
    def on_theme_click(e):
        print("Нажата тема")
        page.snack_bar = ft.SnackBar(
            ft.Text("Открыт раздел темы"),
            bgcolor=GREEN,
        )
        page.snack_bar.open = True
        page.update()
    
    def on_avatar_click(e):
        print("Аватар нажат")
        page.snack_bar = ft.SnackBar(
            ft.Text("Клик по аватару"),
            bgcolor=GREEN,
        )
        page.snack_bar.open = True
        page.update()
    
    def reset_values(e):
        global countChange, countLiters, countRON, setMessage
        
        # Сбрасываем все значения
        countChange = 0
        countLiters = 0
        countRON = 0
        setMessage = "Включены"
        
        # Обновляем все тексты
        changes_display.value = str(countChange)
        liters_display.value = str(countLiters)
        ron_display.value = str(countRON)
        notification_text.value = setMessage
        
        page.snack_bar = ft.SnackBar(
            ft.Text("Все значения обнулены!"),
            bgcolor=GREEN,
        )
        page.snack_bar.open = True
        page.update()
        print("Значения обнулены")
    
    # Создаем аватар с обработчиком через GestureDetector
    avatar = ft.CircleAvatar(
        radius=45,
        bgcolor=GREEN,
        content=ft.Icon(
            ft.Icons.PERSON,
            size=50,
            color=BG,
        ),
    )
    
    avatar_gesture = ft.GestureDetector(
        content=avatar,
        on_tap=on_avatar_click,
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
                            color=TEXT,
                            size=16,
                        ),
                        notification_text,
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
                            color=TEXT,
                            size=16,
                        ),
                        ft.Text(
                            "Лукойл",
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
                            color=TEXT,
                            size=16,
                        ),
                        ft.Text(
                            "Тёмная",
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
                        avatar_gesture,
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
                    ft.Container(
                        expand=True,
                        bgcolor=CARD,
                        border_radius=12,
                        padding=15,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.SYNC,
                                    color=GREEN,
                                ),
                                changes_display,  # Используем объект Text напрямую
                                ft.Text(
                                    "Смешиваний",
                                    size=12,
                                    color=TEXT2,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        bgcolor=CARD,
                        border_radius=12,
                        padding=15,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.LOCAL_GAS_STATION,
                                    color=GREEN,
                                ),
                                liters_display,  # Используем объект Text напрямую
                                ft.Text(
                                    "Литров",
                                    size=12,
                                    color=TEXT2,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        bgcolor=CARD,
                        border_radius=12,
                        padding=15,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.SPEED,
                                    color=GREEN,
                                ),
                                ron_display,  # Используем объект Text напрямую
                                ft.Text(
                                    "Средний RON",
                                    size=12,
                                    color=TEXT2,
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
                color=TEXT,
            ),
            
            ft.Container(
                bgcolor=CARD,
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
                on_click=reset_values,  # Используем функцию сброса
                width=float('inf'),
            ),
        ],
    )