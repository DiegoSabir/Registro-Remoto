import flet as ft
from conexion import authenticate, get_employee_id, get_attendance_records
from menu import menu_view 
from fondo import create_background_container

def main_view(page: ft.Page):
    """
    El contenedor principal contiene el contenido de la pantalla
    """

    email_field = ft.TextField(
        label='Correo electrónico',
        suffix_text="@galvintec.com",
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.EMAIL,
    )
    password_field = ft.TextField(
        label='Contraseña',
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True
    )

    # Crear un SnackBar para las notificaciones
    snack_bar = ft.SnackBar(
        content=ft.Text("Usuario o contraseña incorrectos."),
        action="OK"
    )

    # Añadir el SnackBar a la lista de overlays
    page.overlay.append(snack_bar)

    def show_snack_bar():
        """

        """

        snack_bar.open = True
        page.update()

    def handle_login(e):
        """
        Obtener los valores del email y contraseña
        """

        email = email_field.value + '@galvintec.com'
        password = password_field.value
        
        # Autenticación en Odoo
        uid = authenticate(email, password)
        if uid:
            # Navegar al menú si el usuario existe
            get_attendance_records(uid, password)
            employee_id = get_employee_id(uid, password)
            if employee_id:
                menu_view(page, uid, password, employee_id)
            else:
                show_snack_bar()
        else:
            # Mostrar SnackBar si el usuario no existe
            show_snack_bar() 

    login_form = ft.Column(controls=[
        ft.Container(ft.Image(src='images/logo.jpg', width=60, border_radius=50), alignment=ft.alignment.center),
        ft.Text('Iniciar Sesión', width=360, size=25, weight='w900', text_align='center'),
        ft.Container(email_field, alignment=ft.alignment.center),
        ft.Container(password_field, alignment=ft.alignment.center),
        ft.Container(
            ft.ElevatedButton(content=ft.Text('INICIAR', color='white', weight='w500'),
                            width=280, bgcolor='black', on_click=handle_login),
            alignment=ft.alignment.center
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    # Usar la función create_background_container para el fondo
    body = create_background_container(content=login_form)

    # Añadir el contenido principal a la página
    page.add(body)


def main(page: ft.Page):
    """
    Configuración de la ventana principal
    """

    page.window.width = 600
    page.window.height = 520
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Cargar la vista principal
    main_view(page)

# Inicializar la aplicación
ft.app(target=main)
