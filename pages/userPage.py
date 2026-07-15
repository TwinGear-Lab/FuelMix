import flet as ft
import os
import shutil
import time
import threading

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


def clear_avatars_folder():
    """Удаляет все файлы из папки avatars"""
    try:
        avatars_dir = "avatars"
        if os.path.exists(avatars_dir):
            for file in os.listdir(avatars_dir):
                file_path = os.path.join(avatars_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Удален старый аватар: {file}")
    except Exception as e:
        print(f"Ошибка при очистке папки аватаров: {e}")


def save_avatar_image(file_path):
    """Сохраняет изображение аватара в папку приложения с уникальным именем"""
    try:
        avatars_dir = "avatars"
        if not os.path.exists(avatars_dir):
            os.makedirs(avatars_dir)

        # Получаем расширение файла
        ext = os.path.splitext(file_path)[1]
        # Создаем уникальное имя с timestamp
        timestamp = int(time.time())
        new_filename = f"avatar_{timestamp}{ext}"
        new_path = os.path.join(avatars_dir, new_filename)

        # Копируем файл
        shutil.copy2(file_path, new_path)
        print(f"Аватар сохранен: {new_filename}")
        return new_path
    except Exception as e:
        print(f"Ошибка при сохранении аватара: {e}")
        return None


def get_avatar_from_storage():
    """Получает последний сохраненный аватар"""
    try:
        avatars_dir = "avatars"
        if os.path.exists(avatars_dir):
            # Получаем все файлы аватаров
            files = [f for f in os.listdir(avatars_dir) if f.startswith("avatar_")]
            if files:
                # Сортируем по времени создания (по имени файла)
                files.sort(reverse=True)
                latest_file = files[0]
                print(f"Загружен аватар: {latest_file}")
                return os.path.join(avatars_dir, latest_file)
    except Exception as e:
        print(f"Ошибка при загрузке аватара: {e}")
    return None


def view(page: ft.Page):
    # Создаем FilePicker для выбора файлов
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    page.update()

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

    def reset_values(e):
        global countChange, countLiters, countRON, setMessage

        countChange = 0
        countLiters = 0
        countRON = 0
        setMessage = "Включены"

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

    # ===== ФУНКЦИЯ ДЛЯ ЗАГРУЗКИ АВАТАРА =====
    def on_avatar_click(e):
        """Открывает диалог выбора файла через flet FilePicker"""
        print("Аватар нажат - открываем выбор файла")

        page.snack_bar = ft.SnackBar(
            ft.Text("Открывается диалог выбора файла..."),
            bgcolor=BLUE,
        )
        page.snack_bar.open = True
        page.update()

        # Открываем диалог выбора файлов для изображений
        file_picker.pick_files(
            dialog_title="Выберите изображение для аватара",
            file_type=ft.FilePickerFileType.IMAGE,
            allow_multiple=False,
        )

    # Обработчик выбора файла
    def on_file_selected(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path

            valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
            if file_path.lower().endswith(valid_extensions):
                # Очищаем старые аватары
                clear_avatars_folder()

                # Сохраняем новый аватар с уникальным именем
                saved_path = save_avatar_image(file_path)
                if saved_path:
                    # Обновляем аватар
                    try:
                        # Обновляем содержимое аватара
                        avatar.content = ft.Image(
                            src=saved_path,
                            width=100,
                            height=100,
                            fit="cover",
                        )
                        avatar.bgcolor = None

                        # Принудительно обновляем
                        avatar.update()
                        page.update()

                        page.snack_bar = ft.SnackBar(
                            ft.Text("Аватар успешно обновлен!"),
                            bgcolor=GREEN,
                        )
                        page.snack_bar.open = True
                        page.update()
                    except Exception as err:
                        print(f"Ошибка при обновлении аватара: {err}")
                        # Если ошибка, перезагружаем страницу
                        page.snack_bar = ft.SnackBar(
                            ft.Text("Аватар обновлен! Перезагружаем страницу..."),
                            bgcolor=BLUE,
                        )
                        page.snack_bar.open = True
                        page.update()

                        def reload_page():
                            time.sleep(1)
                            # Переключаем на главную и обратно
                            page.change_page(0)
                            time.sleep(0.1)
                            page.change_page(4)

                        thread = threading.Thread(target=reload_page, daemon=True)
                        thread.start()
                else:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Ошибка при сохранении аватара!"),
                        bgcolor=ft.Colors.RED,
                    )
                    page.snack_bar.open = True
                    page.update()
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Пожалуйста, выберите файл изображения!"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Выбор файла отменен"),
                bgcolor=TEXT2,
            )
            page.snack_bar.open = True
            page.update()

    # Привязываем обработчик выбора файла
    file_picker.on_result = on_file_selected

    # Загружаем сохраненный аватар
    avatar_image_path = get_avatar_from_storage()

    # Создаем аватар
    if avatar_image_path and os.path.exists(avatar_image_path):
        avatar = ft.Container(
            bgcolor=None,
            width=100,
            height=100,
            border_radius=50,
            content=ft.Image(
                src=avatar_image_path,
                width=100,
                height=100,
                fit="cover",
            )
        )
    else:
        avatar = ft.Container(
            bgcolor=GREEN,
            width=100,
            height=100,
            border_radius=50,
            content=ft.Icon(
                ft.Icons.PERSON,
                size=50,
                color=BG,
            )
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
                                changes_display,
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
                                liters_display,
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
                                ron_display,
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
                on_click=reset_values,
                width=float('inf'),
            ),
        ],
    )