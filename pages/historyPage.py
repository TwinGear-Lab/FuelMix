import flet as ft
from history_storage import load_history, clear_history
from datetime import datetime


def view(page: ft.Page):
    # Загружаем историю
    history = load_history()
    print(f"Загрузка истории. Найдено записей: {len(history)}")

    # Создаем контейнер для списка истории
    history_list = ft.Column(spacing=12)

    # Переменные для статистики
    total_calculations = 0
    total_octane = 0
    total_volume = 0

    def refresh_history():
        """Обновляет отображение истории"""
        nonlocal total_calculations, total_octane, total_volume

        history_list.controls.clear()
        history = load_history()
        print(f"Обновление истории. Найдено записей: {len(history)}")

        # Сбрасываем статистику
        total_calculations = 0
        total_octane = 0
        total_volume = 0

        if not history:
            history_list.controls.append(
                ft.Container(
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    border_radius=12,
                    padding=30,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.HISTORY, size=50, color=ft.Colors.GREY_400),
                            ft.Text("История пуста", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Выполните расчет на главной странице", size=14, color=ft.Colors.GREY_400),
                        ]
                    )
                )
            )
        else:
            for idx, record in enumerate(history):
                # Считаем статистику
                total_calculations += 1
                result = record.get("result", {})
                octane = float(result.get("octane", 0))
                volume = float(result.get("volume", 0))
                total_octane += octane
                total_volume += volume

                # Получаем данные
                timestamp = record.get("timestamp", "Неизвестно")
                fuels = record.get("fuels", {})

                # Формируем строку с информацией о топливе
                fuel_parts = []
                azs_parts = []
                volume_parts = []

                # Топливо в баке
                tank = fuels.get("tank", {})
                if tank.get("volume", 0) > 0:
                    tank_type = tank.get("type", "?")
                    tank_azs = tank.get("azs", "")
                    tank_octane_val = tank.get("octane", 0)
                    tank_volume_val = tank.get("volume", 0)
                    fuel_parts.append(f"{tank_type} ({tank_octane_val:.1f})")
                    if tank_azs and tank_azs != "Не выбрана":
                        azs_parts.append(tank_azs)
                    volume_parts.append(f"{tank_volume_val:.1f} л")

                # Топливо 1
                fuel1 = fuels.get("fuel1", {})
                if fuel1.get("volume", 0) > 0:
                    fuel1_type = fuel1.get("type", "?")
                    fuel1_azs = fuel1.get("azs", "")
                    fuel1_octane_val = fuel1.get("octane", 0)
                    fuel1_volume_val = fuel1.get("volume", 0)
                    fuel_parts.append(f"{fuel1_type} ({fuel1_octane_val:.1f})")
                    if fuel1_azs and fuel1_azs != "Не выбрана":
                        azs_parts.append(fuel1_azs)
                    volume_parts.append(f"{fuel1_volume_val:.1f} л")

                # Топливо 2
                fuel2 = fuels.get("fuel2", {})
                if fuel2.get("volume", 0) > 0:
                    fuel2_type = fuel2.get("type", "?")
                    fuel2_azs = fuel2.get("azs", "")
                    fuel2_octane_val = fuel2.get("octane", 0)
                    fuel2_volume_val = fuel2.get("volume", 0)
                    fuel_parts.append(f"{fuel2_type} ({fuel2_octane_val:.1f})")
                    if fuel2_azs and fuel2_azs != "Не выбрана":
                        azs_parts.append(fuel2_azs)
                    volume_parts.append(f"{fuel2_volume_val:.1f} л")

                # Формируем строки для отображения
                fuel_info = " + ".join(fuel_parts) if fuel_parts else "Нет данных"
                azs_info = " + ".join(azs_parts) if azs_parts else "АЗС не указаны"
                volume_info = " + ".join(volume_parts) if volume_parts else "0 л"

                # Форматируем дату и время
                try:
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    date_str = dt.strftime("%d %B %Y")
                    time_str = dt.strftime("%H:%M")
                except:
                    date_str = timestamp.split()[0] if " " in timestamp else timestamp
                    time_str = timestamp.split()[1] if " " in timestamp else ""

                # Получаем итоговый октан
                result_octane = result.get('octane', '?')
                result_volume_val = result.get('volume', '0')

                # Создаем карточку
                history_card = ft.Container(
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    border_radius=12,
                    padding=15,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            # Результат ОЧ и дата
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"#{idx + 1}",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREY_400,
                                    ),
                                    ft.Text(
                                        f"{result_octane}",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREEN,
                                        expand=True,
                                    ),
                                    ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                        controls=[
                                            ft.Text(
                                                date_str,
                                                size=12,
                                                color=ft.Colors.GREY_400,
                                            ),
                                            ft.Text(
                                                time_str,
                                                size=11,
                                                color=ft.Colors.GREY_400,
                                            ),
                                        ],
                                        spacing=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            # Информация о топливе
                            ft.Text(
                                fuel_info,
                                size=15,
                                weight=ft.FontWeight.W_500,
                            ),
                            # АЗС
                            ft.Text(
                                azs_info,
                                size=13,
                                color=ft.Colors.GREY_400,
                            ),
                            # Объем
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.LOCAL_GAS_STATION, size=16, color=ft.Colors.GREY_400),
                                    ft.Text(
                                        f"{volume_info} = {result_volume_val} л",
                                        size=13,
                                        color=ft.Colors.GREY_400,
                                    ),
                                ],
                                spacing=5,
                            ),
                            # Разделитель между карточками (кроме последней)
                            ft.Divider(height=1, color=ft.Colors.GREY_400) if idx < len(
                                history) - 1 else ft.Container(),
                        ]
                    ),
                )
                history_list.controls.append(history_card)

        # Обновляем статистику
        update_stats()
        page.update()

    def update_stats():
        """Обновляет статистику в верхней части страницы"""
        avg_octane = total_octane / total_calculations if total_calculations > 0 else 0

        stats_container.content = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=12,
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
                controls=[
                    ft.Text(
                        "Всего расчетов",
                        size=13,
                        color=ft.Colors.GREY_400,
                    ),
                    ft.Text(
                        str(total_calculations),
                        size=28,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_400),  # Убрал width
                    ft.Text(
                        f"Средний октан: {avg_octane:.1f}",
                        size=16,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Text(
                        f"Общий объем: {total_volume:.1f} л",
                        size=14,
                        color=ft.Colors.GREY_400,
                    ),
                ]
            ),
        )
        page.update()

    def clear_all_history(e):
        """Очищает всю историю с подтверждением"""

        def confirm_clear(e):
            if clear_history():
                refresh_history()
                page.snack_bar = ft.SnackBar(
                    ft.Text("История очищена!"),
                    bgcolor=ft.Colors.GREEN,
                )
                page.snack_bar.open = True
                page.update()
            page.dialog.open = False
            page.update()

        def cancel_clear(e):
            page.dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Очистка истории"),
            content=ft.Text("Вы уверены, что хотите удалить всю историю?"),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_clear),
                ft.TextButton("Очистить", on_click=confirm_clear, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    # Создаем контейнер для статистики
    stats_container = ft.Container()

    # Создаем страницу
    result = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text(
                        "История смешиваний",
                        size=30,
                        weight="bold",
                        expand=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_SWEEP,
                        icon_color=ft.Colors.RED,
                        tooltip="Очистить историю",
                        on_click=clear_all_history,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            stats_container,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),  # Просто для отступа
            # Список истории
            history_list,
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=15,
    )

    # Загружаем историю при создании страницы
    refresh_history()

    return result