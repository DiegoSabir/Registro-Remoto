import flet as ft
from utils.connection import manage_check, verify_assistance, get_user_name
from utils.theme_manager import ThemeManager, get_theme_colors
from .allowance import allowance_view

STORAGE_PREFIX = "galvintec.main_app."

def menu_view(page: ft.Page, uid, password, employee_id):
    page.clean()
    
    page.padding = 20
    page.window_width = 400
    page.window_height = 700
    page.window_resizable = False
    page.title = "Galvintec Menu"

    check_on = verify_assistance(uid, password, employee_id)
    name = get_user_name(uid, password, employee_id)

    def create_button(text, icon, color, on_click, visible=True):
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

    clock_in_button = create_button(
        "Clock In",
        ft.icons.TIMER,
        ft.colors.GREEN,
        lambda _: manage_check(uid, password, employee_id, 'enter', clock_in_button, clock_out_button, page),
        not check_on
    )

    clock_out_button = create_button(
        "Clock Out",
        ft.icons.TIMER_OFF,
        ft.colors.RED,
        lambda _: manage_check(uid, password, employee_id, 'exit', clock_in_button, clock_out_button, page),
        check_on
    )

    theme_manager = ThemeManager(page)

    def update_colors():
        colors = get_theme_colors(theme_manager.is_dark_mode)
        menu_container.bgcolor = colors['background']
        welcome_text.color = colors['accent']
        name_text.color = colors['primary']
        divider.color = colors['secondary']
        gradient_container.gradient.colors = colors['gradient']

    from .signin import signin_view

    def logout(e):
        page.client_storage.set(f"{STORAGE_PREFIX}email", "")
        page.client_storage.set(f"{STORAGE_PREFIX}password", "")
        page.clean()
        signin_view(page)

    welcome_text = ft.Text("Welcome", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    name_text = ft.Text(name, size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    divider = ft.Divider(height=2)

    menu_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Image(src='assets/images/logo.jpg', width=100, height=100, fit=ft.ImageFit.CONTAIN),
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=20)
            ),
            welcome_text,
            name_text,
            divider,
            ft.Container(height=20),
            clock_in_button,
            clock_out_button,
            create_button(
                "Register Allowance",
                ft.icons.ATTACH_MONEY,
                ft.colors.BLUE,
                lambda _: allowance_view(page, uid, password, employee_id)
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
        spacing=15
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

    update_colors()  # Initial color setup
    theme_manager.add_listener(lambda _: update_colors())  # Listen for theme changes

    page.theme_mode = theme_manager.get_theme_mode()
    page.update()

    page.add(gradient_container)