""" IMPORTS """
# Standard Imports
import base64
import os
import json

# Third Libraries
from utils.connection import send_data_invoice, get_products
import flet as ft

# Local Imports
from .background import create_background_container
from .ia import analyze_allowance

def allowance_view(page: ft.Page, uid, password, employee_id):
    """
    Displays the view for registering allowances.

    :param page (ft.Page): The Flet page object where the components are added.
    :param uid (str): User ID for authentication.
    :param password (str): User's password for authentication.
    :param employee_id (str): Employee ID for context in the app.

    :return None
    """
    page.clean()

    title = ft.TextField(label="Title", 
                         width=300,
                         height=50, 
                         on_change=lambda e: update_register_button_state(),
                         content_padding=ft.Padding(5, 3, 5, 3)
                        )
    
    def validate_float(e):
        """
        Ensures the entered value in the cost field is a valid float 
        and limits to two decimal places if needed.

        :param e: Event triggered by changes in the cost field.
        """
        value = e.control.value
        try:
            float_val = float(value)
            parts = value.split(".")
            if len(parts) == 2 and len(parts[1]) > 2:
                e.control.value = "{:.2f}".format(float_val)

        except ValueError:
            e.control.value = ""  
        page.update()

    def validate_int(e):
        """
        Ensures the entered value in the quantity field is a valid integer.

        :param e: Event triggered by changes in the quantity field.
        """
        if not e.control.value.isdigit():
            e.control.value = ""
        page.update()

    cost = ft.TextField(
        label="Cost",
        width=300,
        height=50,
        prefix_icon=ft.icons.MONEY,
        prefix_text="€",
        hint_text="0.00",
        on_change=lambda e: [validate_float(e), update_register_button_state()],
        content_padding=ft.Padding(5, 3, 5, 3)
    )
    
    quantity = ft.TextField(
        label="Quantity",
        width=300,
        height=50,
        on_change=lambda e: [validate_int(e), update_register_button_state()],
        content_padding=ft.Padding(5, 3, 5, 3)
    )

    image_picker = ft.FilePicker(on_result=lambda e: [on_image_selected(e), update_register_button_state()])
    page.overlay.append(image_picker)


    image_button = ft.ElevatedButton(
        text="Attach Photo",
        on_click=lambda e: image_picker.pick_files(allow_multiple=False),
        bgcolor="black",
        color="white"
    )

    # Dropdown to select the product type
    type_field = ft.Dropdown(label="Select Type", width=300)

    def load_products():
        """
        Loads the product options into the dropdown based on data from the server.
        """
        products = get_products(uid, password)
        
        type_field.options = [
            ft.dropdown.Option(text=product['name'], key=product['id'])
            for product in products
        ]
        page.update()


    load_products()

    products = get_products(uid, password)
    
    # Variable to store the selected file path
    selected_file_path = None
    is_form_valid = False

    def on_image_selected(e):
        """
        Handles the selected image file and validates its format.

        :param e: Event triggered by selecting an image file.
        """
        nonlocal selected_file_path
        if e.files:
            file_path = e.files[0].path
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension in ['.jpg', '.jpeg', '.png']:
                selected_file_path = file_path
                image_button.text = "Photo Attached"
                image_button.style = ft.ButtonStyle(bgcolor="grey")
        
            else:
                selected_file_path = None
                snack_bar_error.content.value = "Please select a valid image file (JPG, JPEG, PNG)."
                snack_bar_error.open = True

        else:
            selected_file_path = None
            snack_bar_error.content.value = "No image selected."
            snack_bar_error.open = True
        
        page.update()

    def update_register_button_state():
        """
        Enables or disables the Register button based on the form's completeness.
        """
        
        if all([title.value, cost.value, quantity.value, type_field.value]):
            register_button.disabled = False 
            register_button.style = ft.ButtonStyle(bgcolor="green")
        else:
            register_button.disabled = True 
            register_button.bgcolor = "black"

        page.update()

    image_picker = ft.FilePicker(on_result=on_image_selected)
    page.overlay.append(image_picker)

    image_button = ft.ElevatedButton(
        text="Attach Photo",
        on_click=lambda e: image_picker.pick_files(allow_multiple=False),
        bgcolor="black",
        color="white"
    )


    snack_bar_error = ft.SnackBar(content=ft.Text("Error"), action="OK")
    page.overlay.append(snack_bar_error)
    
    image_picker.on_result = on_image_selected


    def analyze_and_fill_fields():
        """
        Analyze the image using AI and auto-fill fields in the form.
        """
        if selected_file_path:
            tipo_factura, titulo, precio_unitario, cantidad = analyze_allowance(selected_file_path, products)
        
        try:
            # Asignar los datos extraídos a los campos correspondientes
            title.value = titulo  # Asignar el título de la factura (nombre del establecimiento)
            cost.value = str(precio_unitario)  # Asignar el precio unitario (formato de costo)
            quantity.value = str(cantidad)  # Asignar la cantidad de productos (entero)
            type_field.value = tipo_factura
            
            update_register_button_state()
            # Actualizar la interfaz con los nuevos valores
            page.update()

        except Exception as e:
            # Mostrar un mensaje de error si algo salió mal
            snack_bar_error.content.value = f"Error processing AI data: {str(e)}"
            snack_bar_error.open = True
            page.update()


    def register_allowance(e):
        """
        Enables or disables the Register button based on the form's completeness.
        """
        title_value = title.value
        cost_value = cost.value
        quantity_value = quantity.value
        product_id = type_field.value
        
        file_data = None
        if image_picker.result and image_picker.result.files:
            file_path = image_picker.result.files[0].path
            with open(file_path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')

        if send_data_invoice(uid, password, title_value, cost_value, quantity_value, product_id, file_data):
            from .menu import menu_view
            snack_bar.open = True
            page.update()
            menu_view(page, uid, password, employee_id)
        else:
            snack_bar_error.open = True
        page.update()

    # Success and error notifications
    snack_bar = ft.SnackBar(content=ft.Text("Allowance registered"), action="OK")
    snack_bar_error = ft.SnackBar(content=ft.Text("Error"), action="OK")
    page.overlay.append(snack_bar)
    page.overlay.append(snack_bar_error)

    register_button = ft.ElevatedButton(
        content=ft.Text("Register", color="white", weight="bold"),
        bgcolor="black",
        disabled=True,
        on_click=register_allowance
    )

    ia_button = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Text("IA", color="white", weight="bold"),
            bgcolor="black",
            width=90,
            height=90,
            on_click=lambda e: analyze_and_fill_fields()
        ),
        alignment=ft.alignment.center,
        border_radius=45,
        bgcolor="transparent"
    )

    form_content = ft.Column(
        controls=[
            ft.Text("Register Allowance", size=24, weight="bold", color="black", text_align="center"),
            type_field,
            title,
            cost,
            quantity,
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[image_button, register_button],
                    ),
                    ft.Column(
                        controls=[ia_button],
                    ),
                ],
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    form_container = create_background_container(content=form_content)
    page.add(form_container)

    page.update()
