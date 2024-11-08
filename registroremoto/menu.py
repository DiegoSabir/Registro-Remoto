"""Imports"""

#Third Libraries
import flet as ft

#Local Imports
from connection import manage_check, verify_assistance, get_user_name 
from background import create_background_container
from allowance import allowance_view

def menu_view(page: ft.Page, uid, password, employee_id):
    """
    Displays the main menu view of the application.

    :param page (ft.Page): The Flet page object where the components are added.
    :param uid (str): User ID for authentication.
    :param password (str): User's password for authentication.
    :param employee_id (str): The employee's ID used for managing check-in/check-out.

    :return None
    """
    # Clear the page before setting up the menu view
    page.clean()

    # Verify the state of the check-in and get the employee's name
    check_on = verify_assistance(uid, password, employee_id)
    name = get_user_name(uid, password, employee_id)

    clock_in_button = ft.ElevatedButton(
        content=ft.Text("🕘 Clock In", color="white", weight="bold"),
        on_click=lambda e: manage_check(uid, password, employee_id, 'enter', clock_in_button, clock_out_button, page),
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            shape=ft.RoundedRectangleBorder(20),
            bgcolor='#28A745',
        ),
        visible=not check_on
    )

    clock_out_button = ft.ElevatedButton(
        content=ft.Text("🚪 Clock Out", color="white", weight="bold"),
        on_click=lambda e: manage_check(uid, password, employee_id, 'exit', clock_in_button, clock_out_button, page),
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            shape=ft.RoundedRectangleBorder(20),
            bgcolor='#DC3545',
        ),
        visible=check_on 
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
                    on_click=lambda e: allowance_view(page, uid, password, employee_id)
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )

    # Wrap the menu content with a background
    menu_container = create_background_container(content=menu_content)

    # Add the container to the page
    page.add(menu_container)

    # Update the page to reflect the changes
    page.update()
