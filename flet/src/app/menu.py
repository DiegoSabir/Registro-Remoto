"""Imports"""
# Third Imports
import flet as ft

# Local Libraries
from utils.theme_manager import ThemeManager, get_theme_colors
from utils.connection import manage_check, verify_assistance, get_user_name, update_work_hours
from .invoice import invoice_view
from .list import list_view

STORAGE_PREFIX = "galvintec.main_app."

def menu_view(page: ft.Page, uid, password, employee_id):
    """
    Displays the main menu for the application. This menu includes options for 
    clocking in/out, viewing and registering invoices, and logging out.

    Args:
        page (ft.Page): The Flet page instance.
        uid: User ID for authentication.
        password: User password for authentication.
        employee_id: The employee's unique identifier in the system.
    """
    page.clean()

    page.padding = 20
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False
    page.title = "Galvintec Menu"

    check_on = verify_assistance(uid, password, employee_id)
    name = get_user_name(uid, password, employee_id)

    def create_button(text, icon, color, on_click, visible=True):
        """
        Creates a styled button with an icon and specified behavior.

        Args:
            text (str): The label for the button.
            icon: The icon to display on the button.
            color: The background color of the button.
            on_click (function): The callback function to execute when the button is clicked.
            visible (bool): Determines if the button is visible. Defaults to True.

        Returns:
            ft.ElevatedButton: A styled button component.
        """
        return ft.ElevatedButton(
            content=ft.Row(
                [ft.Icon(icon, color=ft.colors.WHITE), ft.Text(text, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=color,
                elevation=5,
            ),
            on_click=on_click,
            width=280,
            height=60,
            visible=visible,
        )

    check_in_text = ft.Text(
        value="",
        italic=True,
        color=ft.colors.BLACK87,
        size=14,
        text_align=ft.TextAlign.CENTER,
        visible=False
    )

    clock_in_button = create_button(
        "Clock In",
        ft.icons.TIMER,
        ft.colors.GREEN,
        lambda _: manage_check(uid, password, employee_id, 'enter', clock_in_button, clock_out_button, page, check_in_text),
        not verify_assistance(uid, password, employee_id)[0]
    )

    clock_out_button = create_button(
        "Clock Out",
        ft.icons.TIMER_OFF,
        ft.colors.RED,
        lambda _: manage_check(uid, password, employee_id, 'exit', clock_in_button, clock_out_button, page, check_in_text),
        verify_assistance(uid, password, employee_id)[0]
    )

    theme_manager = ThemeManager(page)
    
    def update_colors():
        """
        Updates the colors of the UI components in the menu based on the current theme. 
        Adjusts background, text, and gradient colors to match the theme.
        """
        colors = get_theme_colors(theme_manager.is_dark_mode)
        menu_container.bgcolor = colors['background']
        welcome_text = ft.Text("Welcome", size=25, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        name_text = ft.Text(name, size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        divider.color = colors['secondary']
        check_in_text.color = colors['text']
        gradient_container.gradient.colors = colors['gradient']

    def logout(e):
        """
        Logs the user out of the application by clearing stored credentials 
        and navigating back to the sign-in view.

        Args:
            e: The event triggered by the logout button click.
        """
        from .signin import signin_view
        page.client_storage.set(f"{STORAGE_PREFIX}email", "")
        page.client_storage.set(f"{STORAGE_PREFIX}password", "")
        page.clean()
        signin_view(page)

    welcome_text = ft.Text("Welcome", size=25, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    name_text = ft.Text(name, size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    divider = ft.Divider(height=2)

    menu_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Image(
                    src=('../assets/images/user.png'), 
                    width=200, 
                    height=200, 
                    fit=ft.ImageFit.CONTAIN),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=5),
            ),
            welcome_text,
            name_text,
            divider,
            clock_in_button,
            clock_out_button,
            check_in_text,
            create_button(
                "Register Invoice",
                ft.icons.ATTACH_MONEY,
                ft.colors.BLUE,
                lambda _: invoice_view(page, uid, password, employee_id)
            ),
            create_button(
                "Invoice List",
                ft.icons.LIST,
                ft.colors.BROWN,
                lambda _: list_view(page, uid, password, employee_id)
            ),
            ft.Container(height=20),
            create_button(
                "Log out",
                ft.icons.LOGOUT,
                ft.colors.ORANGE,
                logout
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8
    )

    menu_container = ft.Container(
        content=menu_content,
        width=360,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            offset=ft.Offset(0, 0),
        )
    )

    gradient_container = ft.Container(
        content=menu_container,
        alignment=ft.alignment.center,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[]
        )
    )

    update_colors()  
    theme_manager.add_listener(lambda _: update_colors())

    update_work_hours(uid, password, employee_id, check_in_text, page)

    page.theme_mode = theme_manager.get_theme_mode()
    page.update()

    page.add(gradient_container)

