"""Imports"""
# Local Imports
from app.signin import signin_view

#Third Libraries
import flet as ft

def main(page: ft.Page):
    """
    Initializes the main window of the Flet app.
    """
    page.window.width = 800
    page.window.height = 700
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    signin_view(page)

ft.app(target=main)
 