import flet as ft
import os
import shutil
import time
import threading
from theme import get_theme_name, get_theme_colors

GREEN = ft.Colors.GREEN
BLUE = ft.Colors.BLUE

setMessage = "Включены"
countChange = 0
countLiters = 0
countRON = 0

# Глобальная переменная для хранения текущего аватара
current_avatar = None
avatar_gesture_ref = None


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

        ext = os.path.splitext(file_path)[1]
        timestamp = int(time.time())
        new_filename = f"avatar_{timestamp}{ext}"
        new_path = os.path.join(avatars_dir, new_filename)

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
            files = [f for f in os.listdir(avatars_dir) if f.startswith("avatar_")]
            if files:
                files.sort(reverse=True)
                latest_file = files[0]
                print(f"Загружен аватар: {latest_file}")
                return os.path.join(avatars_dir, latest_file)
    except Exception as e:
        print(f"Ошибка при загрузке аватара: {e}")
    return None


def view(page: ft.Page):
    global current_avatar, avatar_gesture_ref

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
        global countChange, countLiters, countRON, setMessage

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

    # ===== ФУНКЦИЯ ДЛЯ ВЫБОРА ФАЙЛА (КРОССПЛАТФОРМЕННАЯ) =====
    def on_avatar_click(e):
        """Открывает диалог выбора файла (кросс-платформенный)"""
        print("Аватар нажат - открываем выбор файла")

        # Создаем FilePicker
        file_picker = ft.FilePicker()

        # Обработчик выбора файла (для разных версий Flet)
        def on_picked(e):
            if e.files:
                selected_file = e.files[0]
                process_selected_file(selected_file.path)
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Выбор файла отменен"),
                    bgcolor=ft.Colors.GREY,
                )
                page.snack_bar.open = True
                page.update()

        # Привязываем обработчик (для совместимости с разными версиями)
        try:
            # Для новых версий Flet
            file_picker.on_result = on_picked
        except:
            # Для старых версий Flet
            file_picker.on_picked = on_picked

        page.overlay.append(file_picker)
        page.update()

        # Открываем диалог выбора файла
        try:
            file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["png", "jpg", "jpeg", "gif", "bmp", "webp"],
                dialog_title="Выберите изображение для аватара"
            )
        except Exception as e:
            print(f"Ошибка при открытии диалога: {e}")
            # Альтернативный способ для некоторых версий
            try:
                file_picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["png", "jpg", "jpeg", "gif", "bmp", "webp"],
                )
            except:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Ошибка открытия диалога выбора файла"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()

    def process_selected_file(file_path):
        """Обрабатывает выбранный файл"""
        global current_avatar

        if not file_path:
            return

        try:
            # Очищаем старые аватары
            clear_avatars_folder()

            # Сохраняем новый аватар
            saved_path = save_avatar_image(file_path)

            if saved_path:
                # Создаем новый аватар
                new_avatar = ft.Container(
                    bgcolor=None,
                    width=100,
                    height=100,
                    border_radius=50,
                    content=ft.Image(
                        src=saved_path,
                        width=100,
                        height=100,
                        fit="cover",
                    )
                )

                # Обновляем глобальную переменную
                current_avatar = new_avatar

                # Обновляем содержимое GestureDetector
                if avatar_gesture_ref:
                    avatar_gesture_ref.content = new_avatar
                    page.update()

                page.snack_bar = ft.SnackBar(
                    ft.Text("Аватар успешно обновлен!"),
                    bgcolor=GREEN,
                )
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Ошибка при сохранении аватара!"),
                    bgcolor=ft.Colors.RED,
                )
                page.snack_bar.open = True
                page.update()
        except Exception as err:
            print(f"Ошибка при обновлении аватара: {err}")
            page.snack_bar = ft.SnackBar(
                ft.Text("Ошибка при обновлении аватара!"),
                bgcolor=ft.Colors.RED,
            )
            page.snack_bar.open = True
            page.update()

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
                color=ft.Colors.WHITE,
            )
        )

    # Сохраняем текущий аватар в глобальную переменную
    current_avatar = avatar

    # Создаем GestureDetector и сохраняем ссылку на него
    avatar_gesture = ft.GestureDetector(
        content=avatar,
        on_tap=on_avatar_click,
    )

    # Сохраняем ссылку на GestureDetector для обновления
    avatar_gesture_ref = avatar_gesture

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

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            # Заголовок
            ft.Text(
                "Профиль",
                size=30,
                weight="bold",
            ),

            # Карточка пользователя
            ft.Container(
                bgcolor=ft.Colors.SURFACE_CONTAINER,
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
                width=float('inf'),
            ),
        ],
    )