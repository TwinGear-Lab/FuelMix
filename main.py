import os
import flet as ft
from pages import homePage
from pages import historyPage
from pages import fuelSettingsUserPage
from pages import mapFuelPage
from pages import userPage
from widgets.navigationPanel import navigation_panel
from theme import current_theme, toggle_theme, MIN_SCREEN_WIDTH_PX  # импортируем из theme.py

def main(page: ft.Page):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # .ico лежит и в корне проекта, и в assets_dir ("images") — берём из assets,
    # чтобы путь совпадал с тем, что использует flet build при сборке exe/shortcut
    page.window.icon = os.path.join(root_dir, "images", "logo.ico")
    page.title = "FuelMix"
    page.theme_mode = current_theme  # используем глобальную тему
    page.padding = 0
    page.spacing = 0

    # Размеры окна: по умолчанию удобны под ~1060px, но окно можно сузить
    # вплоть до MIN_SCREEN_WIDTH_PX (узкие телефоны) — все страницы под это адаптированы
    page.window.width = 400
    page.window.height = 960
    page.window.min_width = MIN_SCREEN_WIDTH_PX
    page.window.min_height = 500
    page.window.resizable = True
    page.window.center()

    content = ft.Container(expand=True)

    page.navigation_bar = navigation_panel(page, 0)

    page.add(content)

    def change_page(index: int):
        if index == 0:
            content.content = homePage.view(page)
        elif index == 1:
            content.content = historyPage.view(page)
        elif index == 2:
            content.content = fuelSettingsUserPage.view(page)
        elif index == 3:
            content.content = None
            page.update()
            content.content = mapFuelPage.view(page)
        elif index == 4:
            content.content = userPage.view(page)

        page.navigation_bar.selected_index = index
        page.update()

    # Функция для смены темы
    def change_theme():
        toggle_theme(page)  # используем функцию из theme.py

    page.change_page = change_page
    page.change_theme = change_theme

    change_page(0)

ft.run(main, assets_dir="images")