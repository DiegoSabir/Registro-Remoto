"""Imports"""
import flet as ft

STORAGE_KEY = "galvintec.theme.is_dark_mode"

class ThemeManager:
    """
    Manages the theme (light or dark mode) for the application. Provides methods
    to toggle themes, persist user preferences, and notify listeners of changes.
    """
    def __init__(self, page: ft.Page):
        """
        Initializes the ThemeManager instance, loading the saved theme preference
        from client storage and setting up an empty list of listeners.

        Args:
            page (ft.Page): The Flet page instance to manage the theme for.
        """
        self.page = page
        self.is_dark_mode = self.page.client_storage.get(STORAGE_KEY) or False
        self.listeners = []

    def toggle_theme(self):
        """
        Toggles the theme mode between light and dark. Saves the new theme mode to 
        client storage and notifies all listeners of the change.
        """
        self.is_dark_mode = not self.is_dark_mode
        self._save_theme()
        self._notify_listeners()

    def set_theme(self, is_dark):
        """
        Sets the theme mode explicitly to light or dark. Saves the specified theme
        mode to client storage and notifies all listeners of the change.

        Args:
            is_dark (bool): True for dark mode, False for light mode.
        """
        self.is_dark_mode = is_dark
        self._save_theme()
        self._notify_listeners()

    def _save_theme(self):
        """
        Saves the current theme mode to client storage for persistence across sessions.
        """
        self.page.client_storage.set(STORAGE_KEY, self.is_dark_mode)

    def get_theme_mode(self):
        """
        Retrieves the current theme mode.

        Returns:
            ft.ThemeMode: Returns `ft.ThemeMode.DARK` if dark mode is active, otherwise 
            returns `ft.ThemeMode.LIGHT`.
        """
        return ft.ThemeMode.DARK if self.is_dark_mode else ft.ThemeMode.LIGHT

    def add_listener(self, listener):
        """
        Adds a listener function to be notified whenever the theme mode changes.

        Args:
            listener (function): A callback function to be executed when the theme changes.
        """
        self.listeners.append(listener)

    def remove_listener(self, listener):
        """
        Removes a previously added listener function.

        Args:
            listener (function): The callback function to remove.
        """
        self.listeners.remove(listener)

    def _notify_listeners(self):
        """
        Notifies all registered listeners of the current theme mode.
        """
        for listener in self.listeners:
            listener(self.is_dark_mode)

def get_theme_colors(is_dark):
    """
    Returns the color palette for the application based on the current theme.

    Args:
        is_dark (bool): True if the dark mode is active, False for light mode.

    Returns:
        dict: A dictionary containing theme colors for:
            - 'background': Background color of the application.
            - 'text': Default text color.
            - 'primary': Primary color for elements like buttons.
            - 'secondary': Secondary color for borders and accents.
            - 'accent': Accent color for highlights.
            - 'gradient': Gradient color array for backgrounds or containers.
    """
    return {
        'background': ft.colors.GREY_900 if is_dark else ft.colors.WHITE,
        'text': ft.colors.WHITE if is_dark else ft.colors.GREY_900,
        'primary': ft.colors.BLUE_400 if is_dark else ft.colors.BLUE_600,
        'secondary': ft.colors.BLUE_200 if is_dark else ft.colors.BLUE_400,
        'accent': ft.colors.BLUE_200 if is_dark else ft.colors.BLUE_900,
        'gradient': [ft.colors.BLUE_GREY_800, ft.colors.BLUE_GREY_900] if is_dark else [ft.colors.BLUE_50, ft.colors.BLUE_100],
    }
