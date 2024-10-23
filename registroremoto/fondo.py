import flet as ft

def create_background_container(content, width=325, height=450):
    """
    Crea un contenedor con el fondo estilizado común para reutilizar en diferentes vistas.
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
