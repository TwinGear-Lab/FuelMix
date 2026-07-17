import os
import flet as ft
from pages import homePage, historyPage, fuelSettingsUserPage, mapFuelPage, userPage
from widgets.navigationPanel import navigation_panel
from theme import current_theme, toggle_theme
import asyncio
import webbrowser

# Глобальные переменные
AD_URL = "https://illustrious-alpaca-8832e4.netlify.app/"


def main(page: ft.Page):
    page.title = "FuelMix"
    page.theme_mode = current_theme
    page.padding = 0
    page.spacing = 0

    # --- Контейнер для основного контента ---
    content_container = ft.Container(
        expand=True,
        padding=0,
    )

    # --- Главный контейнер ---
    main_container = ft.Column(
        spacing=0,
        expand=True,
        controls=[
            content_container,
        ]
    )

    # --- Панель навигации ---
    page.navigation_bar = navigation_panel(page, 0)
    page.add(main_container)

    # --- Смена страниц ---
    def change_page(index: int):
        if index == 0:
            content_container.content = homePage.view(page)
        elif index == 1:
            content_container.content = historyPage.view(page)
        elif index == 2:
            content_container.content = fuelSettingsUserPage.view(page)
        elif index == 3:
            content_container.content = mapFuelPage.view(page)
        elif index == 4:
            content_container.content = userPage.view(page)

        page.navigation_bar.selected_index = index
        page.update()

    # --- Смена темы ---
    def change_theme():
        toggle_theme(page)

    # --- Открытие рекламы в браузере ---
    def open_ad_in_browser():
        """Открывает страницу с рекламой в браузере"""
        webbrowser.open(AD_URL)
        print(f"Открываем рекламу: {AD_URL}")

    # --- Показ рекламы при входе ---
    def show_ad_on_start():
        """Показывает рекламу при входе в приложение"""
        async def show_with_delay():
            await asyncio.sleep(1.5)
            open_ad_in_browser()
        page.run_task(show_with_delay)

    # --- Сохраняем функции ---
    page.change_page = change_page
    page.change_theme = change_theme
    page.open_ad_in_browser = open_ad_in_browser
    page.show_ad_on_start = show_ad_on_start

    # Загружаем главную страницу
    change_page(0)

    # --- ПОКАЗЫВАЕМ РЕКЛАМУ ПРИ ВХОДЕ ---
    show_ad_on_start()


ft.run(main, assets_dir="images")