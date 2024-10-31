# Standard Imports
import base64

# Third Libraries
import flet as ft

# Local Imports
from connection import send_data_invoice, get_products
from background import create_background_container

def allowance_view(page: ft.Page, uid, password):
    """
    Displays the view for registering allowances.

    :param page (ft.Page): The Flet page object where the components are added.
    :param uid (str): User ID for authentication.
    :param password (str): User's password for authentication.

    :return None
    """
    # Clear the current page content before setting up the form
    page.clean()

    # Form fields
    title = ft.TextField(label="Title", width=300)

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
        prefix_icon=ft.icons.MONEY,
        prefix_text="€",
        hint_text="0.00",
        on_change=validate_float  # Attach the float validator
    )
    
    quantity = ft.TextField(
        label="Quantity",
        width=300,
        on_change=validate_int  # Attach the integer validator
    )

    image_picker = ft.FilePicker(on_result=lambda e: print(f"File selected: {e.files[0].name}" if e.files else "No file selected"))
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

    def on_image_selected(e):
        """
        Handles the event when an image is selected.

        :param e: The event object containing the file selection result.

        :return None
        """
        nonlocal selected_file_path
        if e.files:
            selected_file_path = e.files[0].path
            print(f"Image selected: {selected_file_path}")
        else:
            selected_file_path = None
            print("No image selected")
    
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
            snack_bar.open = True
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
        alignment=ft.alignment.center,
        spacing=20
    )

    # Wrap the form content in a background container
    form_container = create_background_container(content=form_content)

    # Add the form container to the page
    page.add(form_container)

    # Update the page
    page.update()
