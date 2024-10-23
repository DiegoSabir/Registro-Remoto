import flet as ft
from conexion import gestionar_fichaje, verificar_asistencia, obtener_nombre_usuario 
from fondo import create_background_container
from dieta import dieta_view

def menu_view(page: ft.Page, uid, password, employee_id):
    # Limpiar la página anterior
    page.clean()

    # Verificar si el usuario ya está fichando
    ya_fichando = verificar_asistencia(uid, password, employee_id)
    nombre = obtener_nombre_usuario(uid, password, employee_id)

    # Crear botones de fichaje con el mismo estilo
    entrada_button = ft.ElevatedButton(
        content=ft.Text("🕘 Fichar Entrada", color="white", weight="bold"),
        on_click=lambda e: gestionar_fichaje(uid, password, employee_id, 'entrada', entrada_button, salida_button, page),
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            shape=ft.RoundedRectangleBorder(20),
            bgcolor='#28A745',
        ),
        visible=not ya_fichando  # Mostrar según el estado de fichaje
    )

    salida_button = ft.ElevatedButton(
        content=ft.Text("🚪 Fichar Salida", color="white", weight="bold"),
        on_click=lambda e: gestionar_fichaje(uid, password, employee_id, 'salida', entrada_button, salida_button, page),
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            shape=ft.RoundedRectangleBorder(20),
            bgcolor='#DC3545',
        ),
        visible=ya_fichando  # Mostrar según el estado de fichaje
    )

    # Crear el contenido del menú
    menu_content = ft.Column(
        controls=[
            ft.Text("Bienvenido al menú: " + nombre, size=24, weight="bold", color="white", text_align="center"),
            ft.Row(
                controls=[entrada_button, salida_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            ft.Container(
                ft.ElevatedButton(
                    content=ft.Text('Agregar dieta de viaje', color='white', weight='w500'),
                    width=280,
                    bgcolor='black',
                    on_click=lambda e: dieta_view(page)
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )

    # Usar la función create_background_container para el fondo
    menu_container = create_background_container(content=menu_content)

    # Agregar el contenedor a la página
    page.add(ft.Container(content=menu_container, alignment=ft.alignment.center, padding=10))

    # Actualizar la página al final
    page.update()
