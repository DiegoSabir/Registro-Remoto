import flet as ft

# Local Imports
from connection import authenticate, get_employee_id, setup_connection
from menu import menu_view
from background import create_background_container

# Define a prefix for client_storage keys
STORAGE_PREFIX = "galvintec.main_app."

# Snackbar for error messages
def show_snack_bar(page, message="User or Password Incorrect"):
    """
    Display a snackbar with a custom message.
    """
    snack_bar = ft.SnackBar(
        content=ft.Text(message),
        action="OK"
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()

# Move `load_stored_data` to a global function
def load_stored_data(page, email_field, password_field, url_field, db_field):
    """
    Load stored data from client_storage and set the fields.
    """
    email = page.client_storage.get(f"{STORAGE_PREFIX}email") or ""
    password = page.client_storage.get(f"{STORAGE_PREFIX}password") or ""
    url = page.client_storage.get(f"{STORAGE_PREFIX}odoo_url") or ""
    db = page.client_storage.get(f"{STORAGE_PREFIX}db_name") or ""
    
    # Assign the loaded values to the fields
    email_field.value = email
    password_field.value = password
    url_field.value = url
    db_field.value = db
    
    # Print the loaded data (for debugging)
    print(f"Loaded data - Email: {email}, Password: {password}, URL: {url}, DB: {db}")

    page.update()

    # Auto authenticate if all values are present
    if email and password and url and db:
        setup_connection(url, db)
        print("Attempting auto-authentication...")
        auto_authenticate(page, email, password, url, db)
    else:
        print("Missing data for automatic authentication.")
        show_snack_bar(page, "Please complete all fields.")
        
def auto_authenticate(page, email, password, url, db):
    """
    Attempt authentication automatically using the stored data.
    """
    uid = authenticate(email, password, url, db)
    if uid:
        employee_id = get_employee_id(uid, password, url, db)
        if employee_id:
            # Store updated data to client_storage
            page.client_storage.set(f"{STORAGE_PREFIX}email", email)
            page.client_storage.set(f"{STORAGE_PREFIX}password", password)
            menu_view(page, uid, password, employee_id)
        else:
            show_snack_bar(page, "Error retrieving employee ID.")
    else:
        show_snack_bar(page, "Authentication failed.")


def main_view(page: ft.Page):
    """
    Sets up the main login view of the application.
    """

    # Define email field
    email_field = ft.TextField(
        label='Email',
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.EMAIL
    )

    # Define password field
    password_field = ft.TextField(
        label='Password',
        width=280,
        height=40,
        color='black',
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True
    )

    # Define URL and DB fields
    url_field = ft.TextField(
        label="URL from Odoo server",
        width=280,
        height=40,
        color='black'
    )
    db_field = ft.TextField(
        label="Database name",
        width=280,
        height=40,
        color='black'
    )

    def handle_login(e):
        """
        Handles the login process when the login button is pressed.
        """
        email = email_field.value
        password = password_field.value
        url = url_field.value
        db = db_field.value

        uid = authenticate(email, password, url, db)
        if uid:
            employee_id = get_employee_id(uid, password, url, db)
            if employee_id:
                page.client_storage.set(f"{STORAGE_PREFIX}email", email_field.value)
                page.client_storage.set(f"{STORAGE_PREFIX}password", password_field.value)
                menu_view(page, uid, password, employee_id)
            else:
                show_snack_bar(page, "Error retrieving employee ID.")
        else:
            show_snack_bar(page, "Authentication failed.")

    def show_update_popup(e=None):
        """
        Show the popup to configure the Odoo server URL and database.
        """
        popup = ft.AlertDialog(
            title=ft.Text("Update Odoo Server Settings"),
            content=ft.Column([url_field, db_field]),
            actions=[
                ft.TextButton("Update", on_click=update_variables),
                ft.TextButton("Cancel", on_click=lambda e: close_popup(popup))
            ],
            actions_alignment=ft.alignment.center,
        )
        page.overlay.append(popup)
        popup.open = True
        page.update()

    def update_variables(e):
        """
        Update the stored variables in client_storage.
        """
        try:
            page.client_storage.set(f"{STORAGE_PREFIX}odoo_url", url_field.value)
            page.client_storage.set(f"{STORAGE_PREFIX}db_name", db_field.value)
            popup = page.overlay[-1]
            close_popup(popup)
            page.update()

        except Exception as e:
            show_snack_bar(page, f"Error updating variables: {str(e)}")

    def close_popup(popup):
        popup.open = False
        page.update()

    # Login form layout
    login_form = ft.Column(
        controls=[
            ft.Container(ft.Image(src='assets/images/logo.jpg', width=60, border_radius=50), alignment=ft.alignment.center),
            ft.Container(ft.Text('Galvintec', width=360, size=25, weight='w900', text_align='center'), alignment=ft.alignment.center),
            ft.Container(email_field, alignment=ft.alignment.center),
            ft.Container(password_field, alignment=ft.alignment.center),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.ElevatedButton(
                    width=280, bgcolor='black', on_click=handle_login,
                    content=ft.Text('Log in', color='white', weight='w500')
                )
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text('or', size=16)
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.ElevatedButton(
                    width=280, bgcolor='black', on_click=show_update_popup,
                    content=ft.Text('Connect to another Odoo server', color='white', weight='w500')
                )
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Wrap the login form in a background container
    body = create_background_container(content=login_form)
    body.alignment = ft.alignment.center

    page.add(body)
    load_stored_data(page, email_field, password_field, url_field, db_field)

def main(page: ft.Page):
    """
    Initializes the main window of the Flet app.
    """
    page.window.width = 800
    page.window.height = 600
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    main_view(page)

# Run the Flet app
ft.app(target=main)
