import flet as ft

# Глобальные переменные для темы
current_theme = ft.ThemeMode.DARK

def toggle_theme(page: ft.Page):
    """Переключает тему приложения"""
    global current_theme
    if current_theme == ft.ThemeMode.DARK:
        current_theme = ft.ThemeMode.LIGHT
    else:
        current_theme = ft.ThemeMode.DARK
    page.theme_mode = current_theme
    page.update()
    return current_theme

def get_theme_name():
    """Возвращает название текущей темы"""
    return "Темная" if current_theme == ft.ThemeMode.DARK else "Светлая"

def constrain_width(content, max_width=760):
    """Центрирует контент и ограничивает его ширину — используется, чтобы
    страницы выглядели аккуратно на экранах шириной ~1060px, а не
    растягивались на всю ширину окна."""
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.TOP_CENTER,
        content=ft.Container(
            width=max_width,
            content=content,
        ),
    )


def get_theme_colors():
    """Возвращает цвета в зависимости от темы"""
    if current_theme == ft.ThemeMode.DARK:
        return {
            "surface": ft.Colors.SURFACE_CONTAINER,  # изменено
            "text": ft.Colors.WHITE,
            "text_secondary": ft.Colors.GREY_400,
            "background": ft.Colors.BLACK,
        }
    else:
        return {
            "surface": ft.Colors.SURFACE_CONTAINER,  # изменено
            "text": ft.Colors.BLACK,
            "text_secondary": ft.Colors.GREY_600,
            "background": ft.Colors.WHITE,
        }