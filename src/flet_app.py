import flet as ft
import asyncio
import json

async def main(page: ft.Page):
    page.title = "Universal AI Scraper"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 800
    page.window_height = 700
    page.padding = 20
    
    
if __name__ == "__main__":
    # Force the app to open as a standard Windows desktop app
    ft.run(target=main, view=ft.AppView.FLET_APP)
    