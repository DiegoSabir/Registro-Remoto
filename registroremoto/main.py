import flet as ft
from conexion import authenticate, get_employee_id, get_attendance_records  # Importar la función de autenticación
from menu import menu_view  # Importar la vista del menú

# El contenedor principal contiene el contenido de la pantalla
def main_view(page: ft.Page):
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
        snack_bar.open = True
        page.update()

    def handle_login(e):
        # Obtener los valores del email y contraseña
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

    body = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls=[
                    # Logo de la empresa
                    ft.Container(ft.Image(src='logo.jpg', width=60, border_radius=50), alignment=ft.alignment.center),
                    # Título Iniciar Sesión
                    ft.Text('Iniciar Sesión', width=360, size=25, weight='w900', text_align='center'),
                    # Campo de texto del correo
                    ft.Container(email_field, alignment=ft.alignment.center),
                    # Campo de texto de la contraseña
                    ft.Container(password_field, alignment=ft.alignment.center),
                    # Checkbox para recordar contraseña
                    ft.Container(ft.Checkbox(label='Recordar contraseña', check_color='black', width=270), alignment=ft.alignment.center),
                    # Botón de Iniciar
                    ft.Container(
                        ft.ElevatedButton(content=ft.Text('INICIAR', color='white', weight='w500'),
                                        width=280, bgcolor='black', on_click=handle_login),
                        alignment=ft.alignment.center
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                gradient=ft.LinearGradient(['#27AFE3', '#EC4A6F']),
                width=325,
                height=450,
                border_radius=20
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        padding=10,
    )

    # Añadir el contenido principal a la página
    page.add(body)


def main(page: ft.Page):
    # Configuración de la ventana principal:
    page.window.width = 600
    page.window.height = 520
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Cargar la vista principal
    main_view(page)

# Inicializar la aplicación
ft.app(target=main)
