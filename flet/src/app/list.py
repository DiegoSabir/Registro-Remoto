"""Imports"""
# Third Imports
import flet as ft

# Local Imports
from utils.theme_manager import ThemeManager, get_theme_colors
from utils.connection import get_employee_expenses, delete_expense

def list_view(page: ft.Page, uid, password, employee_id):
    """
    Displays the expense table view for the user. Lists all employee expenses 
    with options to delete entries and navigate back to the main menu.

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
    page.title = "Expense Table"
 
    expenses = get_employee_expenses(uid, password)

    def handle_delete(e, expense_id):
        """
        Handles the deletion of a specific expense. Refreshes the list view 
        upon successful deletion.

        Args:
            e: The event triggered by the delete button click.
            expense_id: The unique identifier of the expense to delete.
        """
        if delete_expense(uid, password, expense_id, page):
            list_view(page, uid, password, employee_id)

    def go_back():
        """
        Navigates back to the main menu view by clearing the current page 
        and reloading the menu.
        """
        from .menu import menu_view 
        page.clean()
        menu_view(page, uid, password, employee_id)

    theme_manager = ThemeManager(page)

    def update_colors():
        """
        Updates the UI component colors based on the current theme. Adjusts 
        the header, table, and action icons to match the theme's color scheme.
        """
        colors = get_theme_colors(theme_manager.is_dark_mode)
        header.bgcolor = colors['primary']
        header_text.color = colors['text']
        back_button.icon_color = colors['text']
        table_container.border = ft.border.all(1, colors['secondary'])
        table_body_container.border = ft.border.all(1, colors['accent'])
        for row in table_rows:
            row.controls[2].icon_color = ft.colors.RED if theme_manager.is_dark_mode else ft.colors.RED_600
        page.update()

    header_text = ft.Text(
        "Invoice List",
        style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        weight=ft.FontWeight.BOLD,
    )

    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda _: go_back(),
        tooltip="Back to menu",
        icon_size=25,
    )

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: go_back(),
                    tooltip="Back to menu",
                    icon_size=25,
                ),
                ft.Text("Invoice List",
                        style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER, 
                        expand=1), 
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN  
        ),
        border_radius=8,
        padding=ft.padding.all(10),
    )

    table_header = ft.Row(
        controls=[
            ft.Text("   Nombre", weight=ft.FontWeight.BOLD, width=150),
            ft.Text(" Precio", weight=ft.FontWeight.BOLD, width=100),
            ft.Text("Acciones", weight=ft.FontWeight.BOLD, width=100),
        ]
    )

    table_rows = [
        ft.Row(
            controls=[
                ft.Text(expense['name'], width=150),
                ft.Text(f"{expense['unit_amount']}€", width=100),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    on_click=lambda e, id=expense['id']: handle_delete(e, id),
                    tooltip="Eliminar Gasto",
                ),
            ],
        ) for expense in expenses
    ]

    table_body = ft.ListView(
        controls=table_rows,
        spacing=2,
        padding=10,
        auto_scroll=True,
    )

    table_body_container = ft.Container(
        content=table_body,
        height=600,
    )

    table_container = ft.Container(
        content=ft.Column(
            controls=[
                table_header,
                table_body_container,
            ],
        ),
        border_radius=8,
        padding=ft.padding.only(top=10),
    )

    main_column = ft.Column(
        controls=[
            header,
            table_container,
        ],
        spacing=20,
        expand=True,
    )

    page.add(main_column)

    update_colors()
    theme_manager.add_listener(lambda _: update_colors())

    page.theme_mode = theme_manager.get_theme_mode()
    page.update()
