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


# Минимальная ширина экрана, под которую адаптируется интерфейс.
# 85мм при стандартной плотности 96dpi (логические пиксели Flet-окна) —
# запас под совсем узкие телефоны.
MIN_SCREEN_WIDTH_MM = 85
MIN_SCREEN_WIDTH_PX = round(MIN_SCREEN_WIDTH_MM / 25.4 * 96)  # ≈ 321px

PAGE_PADDING = 12  # компактный отступ, чтобы хватало места на узких экранах


def constrain_width(page: ft.Page, content, max_width=760):
    """Центрирует контент и не даёт ему растягиваться сверх max_width на
    широких экранах, но при этом честно сжимается под текущую ширину окна —
    так интерфейс остаётся корректным вплоть до ~128мм (узкие телефоны)."""
    available = (page.width or MIN_SCREEN_WIDTH_PX) - PAGE_PADDING * 2
    width = min(max_width, max(available, 260))
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.TOP_CENTER,
        content=ft.Container(
            width=width,
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