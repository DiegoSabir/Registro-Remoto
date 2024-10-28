"""Imports"""

# Third Libraries
import flet as ft

def create_background_container(content):
    """
    Creates a container with a background for use in different views.

    :param content: The content to be placed inside the container (e.g., text, form, etc.).

    :return ft.Container: A styled container with the specified background settings.
    """
    return ft.Container(
        content=content,
        gradient=ft.LinearGradient(['#27AFE3', '#EC4A6F']),
        width=None,
        height=None,
        expand=True,
        border_radius=20,
        padding=20,
        alignment=ft.alignment.center,
    )
