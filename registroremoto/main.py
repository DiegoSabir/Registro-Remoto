"""IMPORTS"""

# Third Libraries
import flet as ft

# Local Imports
from connection import authenticate, get_employee_id
from credentials import update_env_variable
from menu import menu_view
from background import create_background_container

def main_view(page: ft.Page):
    """
    Sets up the main login view of the application.

    :param page (ft.Page): The Flet page object where the components are added.

    return: None
    """

    # Email input configuration
    email_field = ft.TextField(
        label='Email',
        suffix_text="@galvintec.com",
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.EMAIL,
    )

    # Password input configuration
    password_field = ft.TextField(
        label='Password',
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True
    )
    
    url_field = ft.TextField(
        label="URL from Odoo server",
        width=280,
        height=40,
        color='black',
    )
    db_field = ft.TextField(
        label="Database name",
        width=280,
        height=40,
        color='black',
    )

    # Configuration for error messages
    snack_bar = ft.SnackBar(
        content=ft.Text("User or Password Incorrect"),
        action="OK"
    )

    # Add snackbar to the overlay to be used for error notifications
    page.overlay.append(snack_bar)

    def show_snack_bar(message="User or Password Incorrect"):
        """
        Displays the snackbar to indicate an error during login or updating.

        return: None
        """
        snack_bar.content = ft.Text(message)  # Update the message
        snack_bar.open = True
        page.update()

    def handle_login(e):
        """
        Handles the login process when the login button is clicked.

        return: None
        """
        email = email_field.value + '@galvintec.com'
        password = password_field.value

        # Authenticate with Odoo
        uid = authenticate(email, password)
        if uid:
            # Navigate to the menu if the user is authenticated
            employee_id = get_employee_id(uid, password)
            if employee_id:
                menu_view(page, uid, password, employee_id)
            else:
                show_snack_bar()
        else:
            show_snack_bar()

    '''
    Env configuration section
    '''
    def show_update_popup(e):
        popup = ft.AlertDialog(
            title=ft.Text("Actualizar servidor de Odoo"),
            content=ft.Column([url_field, db_field]),
            actions=[
                ft.TextButton("Actualizar", on_click=update_variables),
                ft.TextButton("Cancelar", on_click=lambda e: close_popup(popup))
            ],
            actions_alignment=ft.alignment.center,
        )
        page.overlay.append(popup)
        popup.open = True
        page.update()

    def update_variables(e):
        try:
            # Agregar comillas a los valores
            url_value = f'"{url_field.value}"'
            db_value = f'"{db_field.value}"'
            
            # Actualizar cada variable en el archivo .env
            update_env_variable('ODOO_URL', url_value)
            update_env_variable('ODOO_DB', db_value)

            # Cerrar el pop-up y mostrar una notificación
            popup = page.overlay[-2]
            close_popup(popup)
            page.overlay.append(snack_bar) == ft.SnackBar(ft.Text("Variables actualizadas correctamente"))
            page.snack_bar.open = True
            page.update()

        except Exception as e:
            # Manejo de excepciones en caso de error
            show_snack_bar(f"Error al actualizar las variables de entorno: {str(e)}")

        except Exception as e:
            # Manejo de excepciones en caso de error
            show_snack_bar("Error al actualizar las variables de entorno. Verifique los valores.")

    def close_popup(popup):
        page.close(popup)
        page.update()
        

    login_form = ft.Column(
    controls=[
        ft.Container(
            ft.Image(src='assets/images/logo.jpg', width=60, border_radius=50),
            alignment=ft.alignment.center
        ),
        ft.Container(
            ft.Text('Galvintec', width=360, size=25, weight='w900', text_align='center'),
            alignment=ft.alignment.center
        ),
        ft.Container(email_field, alignment=ft.alignment.center),
        ft.Container(password_field, alignment=ft.alignment.center),
        ft.Container(
            ft.ElevatedButton(
                content=ft.Text('Log in', color='white', weight='w500'),
                width=280, bgcolor='black', on_click=handle_login
            ),
            alignment=ft.alignment.center
        ),
        ft.Row(
            alignment='center',
            controls=[ft.Text(value='or', size=16)]
        ),
        ft.Container(
            height=40,
            width=280,
            bgcolor='black',
            border_radius=10,
            on_click=show_update_popup,
            alignment=ft.alignment.center,
            content=ft.Row(
                controls=[
                    ft.Image(
                        src='assets/odoo.PNG',
                        width=20,  # Ajuste del tamaño de la imagen para alineación
                        height=20
                    ),
                    ft.Text(
                        value='Connect to another Odoo server',
                        weight='w500',
                        color='white'
                    )
                ],
                alignment=ft.alignment.center
            )
        )
    ],
    alignment=ft.MainAxisAlignment.SPACE_EVENLY
)


    # Wrap the login form with a background container
    body = create_background_container(content=login_form)

    # Add the wrapped login form to the page
    page.add(body)

def main(page: ft.Page):
    """
    Initializes the main Flet application window.

    :param page (ft.Page): The Flet page object where the components are added.

    :return None
    """
    page.window.width = page.window.width  
    page.window.height = page.window.height  
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Display the main login view
    main_view(page)

# Launch the Flet application
ft.app(target=main)
