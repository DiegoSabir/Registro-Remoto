"""Imports"""

# Third Libraries
import flet as ft

def create_background_container(content, width=325, height=450):
    """
    Creates a container with a background for use in different views.

    :param content: The content to be placed inside the container (e.g., text, form, etc.).
    :param width (int, optional): The width of the container. Default is 325.
    :param height (int, optional): The height of the container. Default is 450.

    :return ft.Container: A styled container with the specified background settings.
    """
    return ft.Container(
        content=content,
        gradient=ft.LinearGradient(['#27AFE3', '#EC4A6F']),
        width=width,
        height=height,
        border_radius=20,
        padding=20,
        alignment=ft.alignment.center,
    )
