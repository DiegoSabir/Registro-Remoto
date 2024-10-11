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
        content=ft.Text("Bienvenido al menú de asistencia", size=24, weight="bold", color="blue"),
        alignment=ft.alignment.top_center,
        margin=40  # Cambiado para usar un diccionario
    )
)

    # Crear botones de fichaje
    entrada_button = ft.ElevatedButton(
        text="🕘 Fichar Entrada",
        on_click=lambda e: gestionar_fichaje(uid, password, employee_id, 'entrada', entrada_button, salida_button, page),
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(vertical=40, horizontal=60),
            shape=ft.RoundedRectangleBorder(20),  # Botones con esquinas redondeadas
            bgcolor=('#28A745'),
            color=('#FFFFFF'),
        )
    )

    salida_button = ft.ElevatedButton(
        text="🚪 Fichar Salida",
        on_click=lambda e: gestionar_fichaje(uid, password, employee_id, 'salida', entrada_button, salida_button, page),
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(vertical=40, horizontal=60), 
            shape=ft.RoundedRectangleBorder(20),  # Botones con esquinas redondeadas
            bgcolor=('#DC3545'),
            color=('#FFFFFF'),
            
        )
    )

    # Mostrar solo el botón correspondiente según la verificación
    if ya_fichando:
        salida_button.visible = True
        entrada_button.visible = False  # Ocultar el de entrada
    else:
        entrada_button.visible = True
        salida_button.visible = False  

    # Añadir los botones a la página
    page.add(
        ft.Row(
            controls=[entrada_button, salida_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,  # Espacio entre botones
            wrap=True # Permite que los botones se ajusten si la pantalla es pequeña
        )
    )

    # Actualizar la página al final
    page.update()

