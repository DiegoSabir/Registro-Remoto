# Third Libraries
import xmlrpc.client
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

    # Configuration for the Odoo server URL input
    url_field = ft.TextField(
        label="URL from Odoo server",
        width=280,
        height=40,
        color='black',
    )

    # Configuration for the Database name input
    db_field = ft.TextField(
        label="Database name",
        width=280,
        height=40,
        color='black',
    )

    # Email input configuration
    email_field = ft.TextField(
        label='Email',
        suffix_text="@galvintec.com",
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.EMAIL,
        visible=False,  # Initially hidden
        animate_offset=ft.animation.Animation(1000),  # Animation on offset change
        offset=ft.transform.Offset(0, -0.5)
    )

    # Password input configuration
    password_field = ft.TextField(
        label='Password',
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True,
        visible=False,  # Initially hidden
        animate_offset=ft.animation.Animation(1000),  # Animation on offset change
        offset=ft.transform.Offset(0, -0.5)
    )

    # Configuration for error messages
    snack_bar = ft.SnackBar(
        content=ft.Text("Invalid Odoo Server or Database"),
        action="OK"
    )

    page.overlay.append(snack_bar)

    def show_snack_bar(message="Invalid Odoo Server or Database"):
        snack_bar.content = ft.Text(message)
        snack_bar.open = True
        page.update()

    # Placeholder for the Connect and Login buttons (initialized below)
    connect_button = None
    login_button = None

    def validate_odoo_server(e):
        """
        Validates the Odoo server URL and Database name, then displays additional fields if valid.
        """
        # Placeholder for the actual server and database check
        try:
            url = url_field.value
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            db_url = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/db")
            version_info = common.version()
            db = db_field.value
            db_list = db_url.list()

            if db in db_list:
                # Hide the Connect button and URL/DB fields
                url_field.visible = False
                db_field.visible = False
                connect_button.visible = False

                # Show the Login button and additional fields
                email_field.visible = True
                password_field.visible = True
                login_button.visible = True

                page.update()

            else:
                print(f"La base de datos '{db}' no existe.")
        
        except Exception as e:
            show_snack_bar("Failed to connect to Odoo server.")
            print(f"Connection error: {e}")
            return

    def handle_login(e):
        """
        Handles the login process when the login button is clicked.
        """
        email = email_field.value + '@galvintec.com'
        password = password_field.value

        uid = authenticate(email, password)
        if uid:
            employee_id = get_employee_id(uid, password)
            if employee_id:
                menu_view(page, uid, password, employee_id)
            else:
                show_snack_bar("Invalid employee ID.")
        else:
            show_snack_bar("Login failed, please check your credentials.")

    # Create the Connect button
    connect_button = ft.ElevatedButton(
        text="Connect to Odoo Server",
        on_click=validate_odoo_server,
        width=280,
        bgcolor='black',
        content=ft.Text('Connect', color='white', weight='w500')
    )

    # Create the Login button, initially hidden
    login_button = ft.ElevatedButton(
        text="Login",
        width=280,
        bgcolor='black',
        on_click=handle_login,
        visible=False  # Initially hidden until URL and DB are valid
    )

    # Create main login form
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
            ft.Container(
                url_field,
                alignment=ft.alignment.center
            ),
            ft.Container(
                db_field,
                alignment=ft.alignment.center
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content=connect_button
            ),
            ft.Container(
                email_field,
                alignment=ft.alignment.center
            ),
            ft.Container(
                password_field,
                alignment=ft.alignment.center
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content=login_button
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Wrap login form with a background container
    body = create_background_container(content=login_form)
    body.alignment = ft.alignment.center

    page.add(body)

def main(page: ft.Page):
    page.window.width = 800
    page.window.height = 600
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    main_view(page)

# Launch Flet application
ft.app(target=main)
