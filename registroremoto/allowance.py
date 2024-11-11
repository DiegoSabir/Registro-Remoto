# Standard Imports
import base64
import os

# Third Libraries
import flet as ft

# Local Imports
from connection import send_data_invoice, get_products
from background import create_background_container

def allowance_view(page: ft.Page, uid, password, employee_id):
    """
    Displays the view for registering allowances.

    :param page (ft.Page): The Flet page object where the components are added.
    :param uid (str): User ID for authentication.
    :param password (str): User's password for authentication.
    :param employee_id (str): Employee ID for context in the app.

    :return None
    """
    # Clear the current page content before setting up the form
    page.clean()

    # Form fields
    title = ft.TextField(label="Title", 
                         width=300,
                         height=50, 
                         on_change=lambda e: update_register_button_state(),
                         content_padding=ft.Padding(5, 3, 5, 3)
                         )
    
    def validate_float(e):
        """
        Validates that only float values with up to two decimal places are 
        allowed in the cost field. Clears the field if the input is invalid.
        """
        value = e.control.value
        try:
            # Convert to float to check validity
            float_val = float(value)
            # Split the input by the decimal point
            parts = value.split(".")
            # Check if the decimal part has more than 2 digits
            if len(parts) == 2 and len(parts[1]) > 2:
                e.control.value = "{:.2f}".format(float_val)

        except ValueError:
            e.control.value = ""  
        page.update()

    def validate_int(e):
        """
        Validates that only integer values are allowed in the quantity field.
        Clears the field if the input is invalid.
        """
        if not e.control.value.isdigit():
            e.control.value = ""  # Clear field if not a valid integer
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

    # Load products from Odoo
    def load_products():
        """
        Retrieves the list of products and updates the dropdown options.

        Fetches product names and IDs using the provided authentication 
        credentials and sets them as options in the dropdown field.
        """
        products = get_products(uid, password)
        
        type_field.options = [
            ft.dropdown.Option(text=product['name'], key=product['id'])
            for product in products
        ]
        page.update()

    # Load products into the dropdown when the view is initialized
    load_products()

    # Variable to store the selected file path
    selected_file_path = None
    is_form_valid = False
    
    def on_image_selected(e):
        nonlocal selected_file_path
        if e.files:
            file_path = e.files[0].path
            file_extension = os.path.splitext(file_path)[1].lower()

            # Check if file is an image
            if file_extension in ['.jpg', '.jpeg', '.png']:
                selected_file_path = file_path

                # Update button to indicate attachment
                image_button.text = "Photo Attached"
                image_button.style = ft.ButtonStyle(bgcolor="grey")
            else:
                selected_file_path = None
                # Show error notification if file is not an image
                snack_bar_error.content.value = "Please select a valid image file (JPG, JPEG, PNG)."
                snack_bar_error.open = True

        else:
            selected_file_path = None
            snack_bar_error.content.value = "No image selected."
            snack_bar_error.open = True
        
        page.update()

    def update_register_button_state():
        """
        Updates the state of the register button. 
        Enables the button if all required fields are filled and the image is valid.
        """
        
        if all([title.value, cost.value, quantity.value, type_field.value]):
            register_button.disabled = False  # Habilita el botón
            register_button.style = ft.ButtonStyle(bgcolor="green")  # Cambia el color del botón a verde
        else:
            register_button.disabled = True   # Deshabilita el botón si falta algún campo
            register_button.bgcolor = "black"  # Color de botón deshabilitado

        page.update()

    # FilePicker and Image Button configuration
    image_picker = ft.FilePicker(on_result=on_image_selected)
    page.overlay.append(image_picker)

    image_button = ft.ElevatedButton(
        text="Attach Photo",
        on_click=lambda e: image_picker.pick_files(allow_multiple=False),
        bgcolor="black",
        color="white"
    )

    # Definir snack_bar_error para mensajes de error generales
    snack_bar_error = ft.SnackBar(content=ft.Text("Error"), action="OK")
    page.overlay.append(snack_bar_error)
    
    # Assign the file picker result handler
    image_picker.on_result = on_image_selected

    def register_allowance(e):
        """
        Registers the allowance with the provided details.

        Collects form data, encodes the attached image in base64 (if provided),
        and sends the data for registration. Displays feedback depending on 
        whether the registration was successful or not.
        """
        title_value = title.value
        cost_value = cost.value
        quantity_value = quantity.value
        product_id = type_field.value
        
        # Encode the attached image in base64 if a file is selected
        file_data = None
        if image_picker.result and image_picker.result.files:
            file_path = image_picker.result.files[0].path
            with open(file_path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')

        # Send allowance data for registration
        if send_data_invoice(uid, password, title_value, cost_value, quantity_value, product_id, file_data):
            from menu import menu_view
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

    # Send button
    register_button = ft.ElevatedButton(
        content=ft.Text("Register", color="white", weight="bold"),
        bgcolor="black",
        disabled=True,
        on_click=register_allowance
    )

    # IA button
    ia_button = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Text("IA", color="white", weight="bold"),
            bgcolor="black",
            width=90,
            height=90,
            on_click=lambda e: None
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

    # Wrap the form content in a background container
    form_container = create_background_container(content=form_content)

    # Add the form container to the page
    page.add(form_container)

    # Update the page
    page.update()
