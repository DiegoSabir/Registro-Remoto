"""Imports"""
#Third Libraries
import flet as ft

# Local Imports
from utils.connection import authenticate, get_employee_id, setup_connection
from utils.theme_manager import ThemeManager, get_theme_colors
from .menu import menu_view

STORAGE_PREFIX = "galvintec.main_app."

def show_snack_bar(page, message="User or Password Incorrect"):
    """
    Displays a snack bar notification on the given page with a specified message.
    
    Args:
        page: The Flet page instance where the snack bar will be displayed.
        message (str): The message to show in the snack bar. Defaults to "User or Password Incorrect".
    """
    snack_bar = ft.SnackBar(
        content=ft.Text(message),
        action="OK",
        action_color=ft.colors.BLUE_400,
        bgcolor=ft.colors.GREY_900,
    )
    page.snack_bar = snack_bar
    snack_bar.open = True
    page.update()

def load_stored_data(page, email_field, password_field, url_field, db_field):
    """
    Loads stored user credentials and server details from client storage
    and populates the corresponding fields in the UI. It also attempts
    to authenticate if all fields are provided.
    
    Args:
        page: The Flet page instance.
        email_field: TextField for the email input.
        password_field: TextField for the password input.
        url_field: TextField for the server URL input.
        db_field: TextField for the database name input.
    """
    email = page.client_storage.get(f"{STORAGE_PREFIX}email") or ""
    password = page.client_storage.get(f"{STORAGE_PREFIX}password") or ""
    url = page.client_storage.get(f"{STORAGE_PREFIX}odoo_url") or ""
    db = page.client_storage.get(f"{STORAGE_PREFIX}db_name") or ""
    
    email_field.value = email
    password_field.value = password
    url_field.value = url
    db_field.value = db
    
    page.update()

    if email and password and url and db:
        setup_connection(url, db)
        auto_authenticate(page, email, password, url, db)
    else:
        show_snack_bar(page, "Please complete all fields.")
        
def auto_authenticate(page, email, password, url, db):
    """
    Attempts to authenticate the user automatically using the provided credentials.
    If successful, navigates to the main menu. Otherwise, displays an error message.
    
    Args:
        page: The Flet page instance.
        email (str): User email.
        password (str): User password.
        url (str): Server URL.
        db (str): Database name.
    """
    uid = authenticate(email, password, url, db)
    if uid:
        employee_id = get_employee_id(uid, password, url, db)
        if employee_id:
            page.client_storage.set(f"{STORAGE_PREFIX}email", email)
            page.client_storage.set(f"{STORAGE_PREFIX}password", password)
            menu_view(page, uid, password, employee_id)
        else:
            show_snack_bar(page, "Error retrieving employee ID.")
    else:
        show_snack_bar(page, "Authentication failed.")

def signin_view(page: ft.Page):
    """
    Creates and displays the sign-in view for the application. Sets up the UI,
    handles theme switching, user input, and login actions.
    
    Args:
        page: The Flet page instance.
    """
    page.padding = 0
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False
    page.title = "Galvintec Sign In"
    
    theme_manager = ThemeManager(page)
    page.theme_mode = theme_manager.get_theme_mode()

    def theme_changed(e):
        """
        Toggles between light and dark themes and updates UI elements accordingly.
        
        Args:
            e: The event triggered by theme switch interaction.
        """
        theme_manager.toggle_theme()
        update_colors()
        update_theme_icon()
        page.update()

    def update_colors():
        """
        Updates the colors of the UI elements based on the current theme.
        This method applies theme-specific styles to the form elements and page.
        """
        colors = get_theme_colors(theme_manager.is_dark_mode)
        body.bgcolor = colors['background']
        
        for field in [email_field, password_field, url_field, db_field]:
            field.border_color = colors['secondary']
            field.focused_border_color = colors['primary']
            field.text_style = ft.TextStyle(color=colors['text'])
        
        login_button.style.bgcolor = colors['primary']
        server_button.content.color = colors['primary']
        title.color = colors['accent']
        subtitle.color = ft.colors.GREY_400 if theme_manager.is_dark_mode else ft.colors.GREY_700
        gradient_container.gradient.colors = colors['gradient']
        update_theme_icon()

    def create_text_field(label, icon, password=False):
        """
        Creates a reusable TextField with a consistent style and optional password masking.
        
        Args:
            label (str): The label for the text field.
            icon: The icon to display within the text field.
            password (bool): Whether the field should mask its input as a password. Defaults to False.
            
        Returns:
            ft.TextField: A styled text field.
        """
        return ft.TextField(
            label=label,
            width=300,
            height=50,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_600,
            prefix_icon=icon,
            password=password,
            can_reveal_password=password,
            text_style=ft.TextStyle(color=ft.colors.GREY_900),
        )

    email_field = create_text_field("Email", ft.icons.EMAIL)
    password_field = create_text_field("Password", ft.icons.LOCK, password=True)
    url_field = create_text_field("Odoo Server URL", ft.icons.LINK)
    db_field = create_text_field("Database Name", ft.icons.INBOX)

    theme_switch = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        icon_color=ft.colors.ORANGE,
        icon_size=20,
        tooltip="Switch theme",
        on_click=theme_changed,
    )

    def update_theme_icon():
        """
        Updates the theme switch button's icon and color based on the current theme.
        """
        theme_switch.icon = ft.icons.LIGHT_MODE if theme_manager.is_dark_mode else ft.icons.DARK_MODE
        theme_switch.icon_color = ft.colors.YELLOW if theme_manager.is_dark_mode else ft.colors.BLUE

    def handle_login(e):
        """
        Handles the login process by validating user input, authenticating credentials,
        and navigating to the main menu if successful.
        
        Args:
            e: The event triggered by the login button click.
        """
        email = email_field.value
        password = password_field.value
        url = url_field.value
        db = db_field.value

        if not all([email, password, url, db]):
            show_snack_bar(page, "Please fill in all fields.")
            return

        setup_connection(url, db)
        uid = authenticate(email, password, url, db)
        if uid:
            employee_id = get_employee_id(uid, password, url, db)
            if employee_id:
                page.client_storage.set(f"{STORAGE_PREFIX}email", email)
                page.client_storage.set(f"{STORAGE_PREFIX}password", password)
                page.client_storage.set(f"{STORAGE_PREFIX}odoo_url", url)
                page.client_storage.set(f"{STORAGE_PREFIX}db_name", db)
                menu_view(page, uid, password, employee_id)
            else:
                show_snack_bar(page, "Error retrieving employee ID.")
        else:
            show_snack_bar(page, "Authentication failed.")

    def show_update_popup(e=None):
        """
        Displays a popup to allow the user to update the server URL and database name.
        
        Args:
            e: Optional event triggered by the popup button click.
        """
        colors = get_theme_colors(theme_manager.is_dark_mode)
        
        url_field.text_style = ft.TextStyle(color=colors['text'])
        db_field.text_style = ft.TextStyle(color=colors['text'])
        
        popup = ft.AlertDialog(
            title=ft.Text("Update Odoo Server Settings", 
                         size=20, 
                         weight=ft.FontWeight.BOLD,
                         color=colors['text']),
            content=ft.Column([url_field, db_field], spacing=20),
            actions=[
                ft.ElevatedButton(
                    "Update",
                    on_click=update_variables,
                    style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=colors['primary'])
                ),
                ft.OutlinedButton(
                    "Cancel",
                    on_click=lambda _: close_popup(popup)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=colors['background']
        )
        page.dialog = popup
        popup.open = True
        page.update()

    def update_variables(e):
        """
        Saves the updated server URL and database name to client storage
        and closes the popup.
    
        Args:
            e: The event triggered by the "Update" button click.
        """
        page.client_storage.set(f"{STORAGE_PREFIX}odoo_url", url_field.value)
        page.client_storage.set(f"{STORAGE_PREFIX}db_name", db_field.value)
        close_popup(page.dialog)
        show_snack_bar(page, "Server settings updated successfully.")

    def close_popup(popup):
        """
        Closes the currently open popup dialog.
        
        Args:
            popup: The popup dialog instance to close.
        """
        popup.open = False
        page.update()

    title = ft.Text('Galvintec', size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
    subtitle = ft.Text('Sign In', size=20, color=ft.colors.GREY_700)

    login_button = ft.ElevatedButton(
        content=ft.Text('Log In', size=16),
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_600),
        width=300,
        height=50,
        on_click=handle_login
    )

    server_button = ft.TextButton(
        content=ft.Text('Connect to another Odoo server', size=14, color=ft.colors.BLUE_600),
        on_click=show_update_popup
    )

    login_form = ft.Column(
        controls=[
            ft.Container(
                content=ft.Image(
                    src=("../assets/images/logo.png"), 
                    width=100,
                    height=100, 
                    fit=ft.ImageFit.CONTAIN),
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=20)
            ),
            title,
            subtitle,
            ft.Container(height=20),
            email_field,
            ft.Container(height=10),
            password_field,
            ft.Container(height=20),
            login_button,
            ft.Container(height=10),
            server_button,
            theme_switch,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    body = ft.Container(
        content=login_form,
        alignment=ft.alignment.center,
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        width=360,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
        )
    )

    gradient_container = ft.Container(
        content=body,
        alignment=ft.alignment.center,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.BLUE_50, ft.colors.BLUE_100]
        )
    )

    update_colors()
    theme_manager.add_listener(lambda _: update_colors())
    
    page.add(gradient_container)
    load_stored_data(page, email_field, password_field, url_field, db_field)
