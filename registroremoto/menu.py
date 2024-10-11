import flet as ft
from conexion import gestionar_fichaje, verificar_asistencia  # Importa la función gestionar_fichaje

def menu_view(page: ft.Page, uid, password, employee_id):
    # Limpiar la página anterior
    page.clean()

    # Verificar si el usuario ya está fichando
    ya_fichando = verificar_asistencia(uid, password, employee_id)

    # Crear el contenido del menú
    page.add(
        ft.Container(
            content=ft.Text("Bienvenido al menú de asistencias", size=30, weight="bold"),
            alignment=ft.alignment.center
        )
    )

    # Crear botones de fichaje
    entrada_button = ft.ElevatedButton(
        text="Fichar Entrada",
        on_click=lambda e: gestionar_fichaje(uid, password, employee_id, 'entrada', entrada_button, salida_button, page)
    )

    salida_button = ft.ElevatedButton(
        text="Fichar Salida",
        on_click=lambda e: gestionar_fichaje(uid, password, employee_id, 'salida', entrada_button, salida_button, page)
    )

    # Mostrar solo el botón correspondiente según la verificación
    if ya_fichando:
        # El usuario ya ha fichado, mostrar solo el botón de salida
        salida_button.visible = True
        entrada_button.visible = False  # Ocultar el de entrada
    else:
        # El usuario no ha fichado, mostrar solo el botón de entrada
        entrada_button.visible = True
        salida_button.visible = False  # Ocultar el de salida

    if ya_fichando:
        page.add(salida_button)
        page.add(entrada_button)
    else:
        page.add(entrada_button)
        page.add(salida_button)

    # Actualizar la página al final
    page.update()
