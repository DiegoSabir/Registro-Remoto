"""IMPORTS"""

# Third Libraries
import flet as ft

# Local Imports
from connection import authenticate, get_employee_id
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

    # Configuration for error menssages
    snack_bar = ft.SnackBar(
        content=ft.Text("User or Password Incorrect"),
        action="OK"
    )

    # Add snackbar to the overlay to be used for error notifications
    page.overlay.append(snack_bar)

    def show_snack_bar():
        """
        Displays the snackbar to indicate an error during login.

        return: None
        """
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

    # Creating the login form layout
    login_form = ft.Column(controls=[
        ft.Container(ft.Image(src='assets/images/logo.jpg', width=60, border_radius=50), alignment=ft.alignment.center),
        ft.Container(ft.Text('Galvintec', width=360, size=25, weight='w900', text_align='center'), alignment=ft.alignment.center),
        ft.Container(email_field, alignment=ft.alignment.center),
        ft.Container(password_field, alignment=ft.alignment.center),
        ft.Container(
            ft.ElevatedButton(content=ft.Text('Log in', color='white', weight='w500'),
                            width=280, bgcolor='black', on_click=handle_login),
            alignment=ft.alignment.center
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

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
