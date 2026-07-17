import os
import flet as ft
import flet_ads as fta
from pages import homePage
from pages import historyPage
from pages import fuelSettingsUserPage
from pages import mapFuelPage
from pages import userPage
from widgets.navigationPanel import navigation_panel
from theme import current_theme, toggle_theme

# Тестовые Ad Unit ID для Android и iOS
TEST_IDS = {
    ft.PagePlatform.ANDROID: {
        "interstitial": "ca-app-pub-3940256099942544/1033173712",
    },
    ft.PagePlatform.IOS: {
        "interstitial": "ca-app-pub-3940256099942544/4411468910",
    },
}


def main(page: ft.Page):
    page.title = "FuelMix"
    page.theme_mode = current_theme
    page.padding = 0
    page.spacing = 0

    # Создаем контейнер для основного контента
    content = ft.Container(expand=True)
    page.navigation_bar = navigation_panel(page, 0)
    page.add(content)

    # --- Функция смены страниц ---
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

    # --- Функция для смены темы ---
    def change_theme():
        toggle_theme(page)

    # --- Логика показа рекламы ---

    # Переменная для хранения объекта рекламы и флага, что она показана
    interstitial_ad = None
    ad_shown = False

    def get_interstitial_ad():
        """Создает и возвращает новый объект InterstitialAd."""
        unit_id = TEST_IDS.get(page.platform, {}).get("interstitial")
        if not unit_id:
            print("Реклама не поддерживается на этой платформе")
            return None

        # Определяем обработчики событий рекламы
        def on_ad_load(e):
            print("Реклама загружена")
            # Автоматически показываем, как только загрузилась
            page.run_task(interstitial_ad.show)

        def on_ad_error(e):
            nonlocal ad_shown
            print(f"Ошибка загрузки рекламы: {e.data}")
            ad_shown = True

        def on_ad_close(e):
            nonlocal ad_shown, interstitial_ad
            print("Реклама закрыта")
            ad_shown = True
            # Удаляем старую рекламу из оверлея
            if interstitial_ad in page.overlay:
                page.overlay.remove(interstitial_ad)
            page.update()

        return fta.InterstitialAd(
            unit_id=unit_id,
            on_load=on_ad_load,
            on_error=on_ad_error,
            on_open=lambda e: print("Реклама открыта"),
            on_close=on_ad_close,
            on_impression=lambda e: print("Показ рекламы засчитан"),
            on_click=lambda e: print("Клик по рекламе"),
        )

    def show_interstitial_ad():
        """Пытается создать и показать межстраничную рекламу."""
        nonlocal ad_shown, interstitial_ad

        if ad_shown:
            print("Реклама уже была показана в этом сеансе")
            return

        # Создаем новый экземпляр
        interstitial_ad = get_interstitial_ad()
        if not interstitial_ad:
            return

        # Добавляем рекламный объект в оверлей страницы
        page.overlay.append(interstitial_ad)
        page.update()
        # Реклама начнет загружаться автоматически

    # --- Сохраняем функции ---
    page.change_page = change_page
    page.change_theme = change_theme

    # Загружаем начальную страницу
    change_page(0)

    # ✅ ПОКАЗЫВАЕМ РЕКЛАМУ СРАЗУ ПОСЛЕ ЗАГРУЗКИ СТРАНИЦЫ
    # Небольшая задержка в 0.5 секунды, чтобы страница успела отрисоваться
    async def show_ad_immediately():
        import asyncio
        await asyncio.sleep(0.5)  # Небольшая задержка для отрисовки UI
        show_interstitial_ad()

    page.run_task(show_ad_immediately)

print("ww")

ft.run(main, assets_dir="images")