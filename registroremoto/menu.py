"""Imports"""

#Third Libraries
import flet as ft

#Local Imports
from connection import manage_check, verify_assistance, get_user_name 
from background import create_background_container
from allowance import allowance_view

def menu_view(page: ft.Page, uid, password, employee_id):
    """
    asdasd
    """

    page.clean()

    # Verify state of check and get name of the employee
    check_on = verify_assistance(uid, password, employee_id)
    name = get_user_name(uid, password, employee_id)

    clock_in_button = ft.ElevatedButton(
        content=ft.Text("🕘 Clock In", color="white", weight="bold"),
        on_click=lambda e: manage_check(uid, password, employee_id, 'entrada', clock_in_button, clock_out_button, page),
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            shape=ft.RoundedRectangleBorder(20),
            bgcolor='#28A745',
        ),
        visible=not check_on
    )

    clock_out_button = ft.ElevatedButton(
        content=ft.Text("🚪 Clock Out", color="white", weight="bold"),
        on_click=lambda e: manage_check(uid, password, employee_id, 'salida', clock_in_button, clock_out_button, page),
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            shape=ft.RoundedRectangleBorder(20),
            bgcolor='#DC3545',
        ),
        visible=check_on  # Show by check state
    )


    menu_content = ft.Column(
        controls=[
            ft.Text("Welcome: \n" + name, size=24, weight="bold", color="white", text_align="center"),
            ft.Row(
                controls=[clock_in_button, clock_out_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            ft.Container(
                ft.ElevatedButton(
                    content=ft.Text('Register Allowance', color='white', weight='w500'),
                    width=280,
                    bgcolor='black',
                    on_click=lambda e: allowance_view(page, uid, password)
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )

    # Use the function create_background
    menu_container = create_background_container(content=menu_content)

    # Add the container to the page
    page.add(ft.Container(content=menu_container, alignment=ft.alignment.center, padding=10))


    page.update()
