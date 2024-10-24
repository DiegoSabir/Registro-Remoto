"""
Imports
"""
# Standard Imports
import base64

# Third Libraries
import flet as ft

# Local Imports
from connection import send_data_invoice, get_products
from background import create_background_container

def allowance_view(page: ft.Page, uid, password):
    """
    Vista para registrar las dietas.
    """

    page.clean()

    # Form fields
    title = ft.TextField(label="Title", width=300)
    cost = ft.TextField(label="Cost", width=300, prefix_icon=ft.icons.MONEY, prefix_text="€", hint_text="0.00")
    quantity = ft.TextField(label="Quantity", width=300)

    image_picker = ft.FilePicker(on_result=lambda e: print(f"File selected: {e.files[0].name}" if e.files else "No file selected"))
    page.overlay.append(image_picker)

    image_button = ft.ElevatedButton(
        text="Attach Photo",
        on_click=lambda e: image_picker.pick_files(allow_multiple=False),
        bgcolor="black",
        color="white"
    )

    # Dropdown to select products
    type_field = ft.Dropdown(label="Select Type", width=300)

    # Load products from Odoo
    def load_products():
        """
        asdadwawd
        """
        products = get_products(uid, password)
        
        type_field.options = [
            ft.dropdown.Option(text=product['name'], key=product['id'])
            for product in products
        ]
        page.update()

    load_products()

    selected_file_path = None

    def on_image_selected(e):
        """
        asdasdad
        """
        nonlocal selected_file_path
        if e.files:
            selected_file_path = e.files[0].path
            print(f"Image selected: {selected_file_path}")
        else:
            selected_file_path = None
            print("No image selected")
    
    image_picker.on_result = on_image_selected

    def register_allowance():
        """
        asdsadsada
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
            snack_bar.open = True
        else:
            snack_bar_error.open = True
        page.update()

    # Definir SnackBars
    snack_bar = ft.SnackBar(content=ft.Text("Allowance registered"), action="OK")
    snack_bar_error = ft.SnackBar(content=ft.Text("Error"), action="OK")
    page.overlay.append(snack_bar)
    page.overlay.append(snack_bar_error)

    # Botón de enviar
    register_button = ft.ElevatedButton(
        content=ft.Text("Register", color="white", weight="bold"),
        bgcolor="black",
        on_click=register_allowance
    )

    # Botón de IA
    ia_button = ft.ElevatedButton(
        content=ft.Text("IA", color="white", weight="bold"),
        bgcolor="black",
        width=90,
        on_click=lambda e: None
    )

    # Contenedor del formulario
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
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Aplicar el fondo usando create_background_container
    form_container = create_background_container(content=form_content)

    # Agregar el contenedor a la página
    page.add(ft.Container(content=form_container, alignment=ft.alignment.center, padding=10))

    # Actualizar la página
    page.update()
