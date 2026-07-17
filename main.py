import os
import flet as ft
from flet_webview import WebView
from pages import homePage, historyPage, fuelSettingsUserPage, mapFuelPage, userPage
from widgets.navigationPanel import navigation_panel
from theme import current_theme, toggle_theme
import asyncio

# Глобальные переменные для управления рекламой
ad_shown = False
ad_container = None
ad_closed = False


def main(page: ft.Page):
    global ad_shown, ad_container, ad_closed

    page.title = "FuelMix"
    page.theme_mode = current_theme
    page.padding = 40
    page.spacing = 0

    # Контейнер для основного контента
    content = ft.Container(expand=True)
    page.navigation_bar = navigation_panel(page, 0)
    page.add(content)

    # --- Смена страниц ---
    def change_page(index: int):
        if index == 0:
            content.content = homePage.view(page)
        elif index == 1:
            content.content = historyPage.view(page)
        elif index == 2:
            content.content = fuelSettingsUserPage.view(page)
        elif index == 3:
            content.content = mapFuelPage.view(page)
        elif index == 4:
            content.content = userPage.view(page)

        page.navigation_bar.selected_index = index
        page.update()

    # --- Смена темы ---
    def change_theme():
        toggle_theme(page)

    # --- Закрытие рекламы ---
    def close_ad(e=None):
        global ad_shown, ad_container, ad_closed
        ad_closed = True
        ad_shown = True

        if ad_container and ad_container in page.overlay:
            page.overlay.remove(ad_container)
            ad_container = None
        page.update()

    def on_webview_error(e):
        """Ошибка загрузки WebView"""
        print(f"Ошибка WebView: {e}")
        # В случае ошибки закрываем рекламу через 2 секунды
        async def close_after_error():
            await asyncio.sleep(2)
            close_ad(None)
        page.run_task(close_after_error)

    # --- Показ рекламы Яндекса ---
    def show_yandex_ad():
        global ad_shown, ad_container, ad_closed

        if ad_shown:
            print("Реклама уже показана")
            return

        # Путь к HTML файлу
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        ad_html_path = os.path.join(assets_dir, "ad_yandex.html")

        # Проверяем существует ли файл
        if not os.path.exists(ad_html_path):
            print(f"Файл рекламы не найден: {ad_html_path}")
            ad_shown = True  # Чтобы не пытаться снова
            return

        # Создаем WebView
        webview = WebView(
            url=ad_html_path,
            expand=True,
            on_web_resource_error=on_webview_error,
        )

        # Контейнер для WebView (затемнение фона)
        ad_container = ft.Container(
            content=ft.Column(
                controls=[
                    webview,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=ft.Colors.BLACK,
            padding=10,
        )

        # Добавляем в оверлей
        page.overlay.append(ad_container)
        page.update()

        # Автозакрытие через 15 секунд (максимальное время показа)
        async def auto_close():
            global ad_closed
            await asyncio.sleep(15)
            if not ad_closed:
                print("Автозакрытие рекламы")
                close_ad(None)

        page.run_task(auto_close)

        # Ждем загрузки WebView и пытаемся внедрить JavaScript-мост
        async def setup_js_bridge():
            await asyncio.sleep(1)
            try:
                # Внедряем функцию для закрытия из JavaScript
                webview.evaluate_javascript("""
                    window.flet = {
                        closeAd: function() {
                            console.log('JS: закрыть рекламу');
                        }
                    };
                    console.log('JS bridge установлен');
                """)
            except Exception as e:
                print(f"Ошибка внедрения JS: {e}")

        page.run_task(setup_js_bridge)

    # --- Сохраняем функции в page ---
    page.change_page = change_page
    page.change_theme = change_theme
    page.show_yandex_ad = show_yandex_ad
    page.close_ad = close_ad

    # Загружаем главную страницу
    change_page(0)

    # --- ПОКАЗ РЕКЛАМЫ ПРИ ЗАПУСКЕ ---
    async def show_ad_on_start():
        await asyncio.sleep(1.5)  # Даем UI отрисоваться
        show_yandex_ad()

    page.run_task(show_ad_on_start)


ft.run(main, assets_dir="images")