"""Imports"""

#Third Libraries
from utils.connection import manage_check, verify_assistance, get_user_name 
import flet as ft

#Local Imports
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

    from .signin import signin_view

    def logout(e):
        page.client_storage.set(f"{STORAGE_PREFIX}email", "")
        page.client_storage.set(f"{STORAGE_PREFIX}password", "")
        page.clean()
        signin_view(page)

    menu_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Image(src='assets/images/logo.jpg', width=100, height=100, fit=ft.ImageFit.CONTAIN),
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=20)
            ),
            ft.Text("Welcome", size=24, color=ft.colors.BLUE_GREY_800 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_GREY_200, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Text(name, size=28, color=ft.colors.BLUE_600 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_300, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(height=2, color=ft.colors.BLUE_200 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLUE_700),
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
        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.GREY_900,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.colors.BLUE_GREY_300 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK,
            offset=ft.Offset(0, 0),
        )
    )

    page.add(
        ft.Container(
            content=menu_container,
            alignment=ft.alignment.center,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.BLUE_50, ft.colors.BLUE_100] if page.theme_mode == ft.ThemeMode.LIGHT else [ft.colors.GREY_900, ft.colors.GREY_800]
            )
        )
    )
    page.update()