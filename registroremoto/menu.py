import flet as ft

def menu_view(page: ft.Page):
    # Crear el contenido de la pantalla de menú
    page.clean()  # Limpiar la página anterior
    page.add(
        ft.Container(
            content=ft.Text("ESTO ES EL MENU", size=30),
            alignment=ft.alignment.center
        )
    )
