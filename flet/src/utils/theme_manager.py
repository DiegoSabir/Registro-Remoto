import flet as ft

STORAGE_KEY = "galvintec.theme.is_dark_mode"

class ThemeManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.is_dark_mode = self.page.client_storage.get(STORAGE_KEY) or False
        self.listeners = []

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self._save_theme()
        self._notify_listeners()

    def set_theme(self, is_dark):
        self.is_dark_mode = is_dark
        self._save_theme()
        self._notify_listeners()

    def _save_theme(self):
        self.page.client_storage.set(STORAGE_KEY, self.is_dark_mode)

    def get_theme_mode(self):
        return ft.ThemeMode.DARK if self.is_dark_mode else ft.ThemeMode.LIGHT

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def _notify_listeners(self):
        for listener in self.listeners:
            listener(self.is_dark_mode)

def get_theme_colors(is_dark):
    return {
        'background': ft.colors.GREY_900 if is_dark else ft.colors.WHITE,
        'text': ft.colors.WHITE if is_dark else ft.colors.GREY_900,
        'primary': ft.colors.BLUE_400 if is_dark else ft.colors.BLUE_600,
        'secondary': ft.colors.BLUE_200 if is_dark else ft.colors.BLUE_400,
        'accent': ft.colors.BLUE_200 if is_dark else ft.colors.BLUE_900,
        'gradient': [ft.colors.BLUE_GREY_800, ft.colors.BLUE_GREY_900] if is_dark else [ft.colors.BLUE_50, ft.colors.BLUE_100],
    }
