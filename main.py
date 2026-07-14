import flet as ft

from pages import homePage
from pages import historyPage
from pages import fuelSettingsUserPage
from pages import mapFuelPage
from pages import userPage

from widgets.navigationPanel import navigation_panel


def main(page: ft.Page):

    page.title = "FuelMix"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.scroll = ft.ScrollMode.AUTO


    # контейнер для текущей страницы
    content = ft.Container(
        expand=True
    )


    def change_page(index):

        if index == 0:
            content.content = homePage.view(page)

        elif index == 1:
            content.content = historyPage.view(page)

        elif index == 2:
            content.content = fuelSettingsUserPage.view(page)

        elif index == 3:
            content.content = mapFuelPage.view(page)

        elif index == 4:
            #content.content = userPage.view(page)
            pass


        page.navigation_bar = navigation_panel(page, index)

        page.update()


    # функция доступна navigationPanel
    page.change_page = change_page


    page.add(content)


    # стартовая страница
    change_page(0)


ft.app(target=main)