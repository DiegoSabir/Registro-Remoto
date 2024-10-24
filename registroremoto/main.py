"""IMPORTS"""

# Third Libraries
import flet as ft

# Local Imports
from connection import authenticate, get_employee_id
from menu import menu_view
from background import create_background_container

def main_view(page: ft.Page):
    """
    asdsadsasd
    """
    email_field = ft.TextField(
        label='Email',
        suffix_text="@galvintec.com",
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.EMAIL,
    )
    password_field = ft.TextField(
        label='Password',
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True
    )

    snack_bar = ft.SnackBar(
        content=ft.Text("User or Password Incorrect"),
        action="OK"
    )

    # Add snackbar to the overlay
    page.overlay.append(snack_bar)

    def show_snack_bar():
        """

        """
        snack_bar.open = True
        page.update()

    def handle_login(e):
        """
        Get the email and password from the user
        """
        email = email_field.value + '@galvintec.com'
        password = password_field.value

        # authenticate with Odoo
        uid = authenticate(email, password)
        if uid:
            # Navegar al menú si el usuario existe
            employee_id = get_employee_id(uid, password)
            if employee_id:
                menu_view(page, uid, password, employee_id)
            else:
                show_snack_bar()
        else:
            show_snack_bar()

    login_form = ft.Column(controls=[
        ft.Container(ft.Image(src='images/logo.jpg', width=60, border_radius=50), alignment=ft.alignment.center),
        ft.Text('Galvintec', width=360, size=25, weight='w900', text_align='center'),
        ft.Container(email_field, alignment=ft.alignment.center),
        ft.Container(password_field, alignment=ft.alignment.center),
        ft.Container(
            ft.ElevatedButton(content=ft.Text('Log in', color='white', weight='w500'),
                            width=280, bgcolor='black', on_click=handle_login),
            alignment=ft.alignment.center
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    # Use the function create_background
    body = create_background_container(content=login_form)

    # add content to the main_view
    page.add(body)


def main(page: ft.Page):
    """
    asdasd
    """
    page.window.width = 600
    page.window.height = 520
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Load main_view
    main_view(page)

# Start the app
ft.app(target=main)
