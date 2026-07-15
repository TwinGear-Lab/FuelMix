import os
import flet as ft
from pages import homePage
from pages import historyPage
from pages import fuelSettingsUserPage
from pages import mapFuelPage
from pages import userPage
from widgets.navigationPanel import navigation_panel
from theme import current_theme, toggle_theme  # импортируем из theme.py

def main(page: ft.Page):
    page.title = "FuelMix"
    page.theme_mode = current_theme  # используем глобальную тему
    page.padding = 0
    page.spacing = 0

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