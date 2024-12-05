"""Imports"""
# Third Imports
import base64
import flet as ft

# Local Imports
from utils.theme_manager import ThemeManager, get_theme_colors
from utils.connection import send_data_invoice, get_products
from .ia import analyze_invoice


def invoice_view(page: ft.Page, uid, password, employee_id):
    """
    Displays the invoice registration view. Sets up the UI for inputting
    invoice details, attaching photos, and analyzing invoice data using AI.

    Args:
        page (ft.Page): The Flet page instance.
        uid: User ID for authentication.
        password: User password for authentication.
        employee_id: The employee's unique identifier in the system.
    """
    page.clean()
    page.bgcolor = ft.colors.BLUE_50
    page.padding = 20
    page.window_width = 400
    page.window_height = 700
    page.window_resizable = False
    page.title = "Galvintec Invoice Registration"

    theme_manager = ThemeManager(page)

    def update_colors():
        """
        Updates the colors of the UI components based on the current theme.
        Applies theme-specific styles to fields, text, and containers.
        """
        colors = get_theme_colors(theme_manager.is_dark_mode)
        page.bgcolor = colors['background']
        form_container.bgcolor = colors['background']
        title_text.color = colors['accent']
        divider.color = colors['secondary']

        for field in [title, cost, quantity, type_field]:
            field.border_color = colors['secondary']
            field.focused_border_color = colors['primary']
            field.text_style = ft.TextStyle(color=colors['text'])

    def create_text_field(label, width=300, prefix_icon=None, prefix_text=None, hint_text=None, validator=None):
        """
        Creates a styled TextField with optional validators and UI enhancements.

        Args:
            label (str): The label for the text field.
            width (int): The width of the text field. Defaults to 300.
            prefix_icon: Optional icon to display inside the text field.
            prefix_text (str): Optional prefix text for the field.
            hint_text (str): Placeholder text to display when the field is empty.
            validator (function): Function to validate the field's input.

        Returns:
            ft.TextField: A configured text field component.
        """
        return ft.TextField(
            label=label,
            width=width,
            height=50,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_600,
            prefix_icon=prefix_icon,
            prefix_text=prefix_text,
            hint_text=hint_text,
            on_change=lambda e: [validator(e) if validator else None, update_register_button_state()],
            text_style=ft.TextStyle(color=ft.colors.GREY_900),
        )

    def validate_float(e):
        """
        Validates and formats the input as a float with up to two decimal places.

        Args:
            e: The event triggered by changes in the text field.
        """
        value = e.control.value
        if value == "":
            return
        value = ''.join(char for char in value if char.isdigit() or char == '.')
        parts = value.split('.')
        if len(parts) > 2:
            value = f"{parts[0]}.{''.join(parts[1:])}"
        if '.' in value:
            integer_part, decimal_part = value.split('.')
            value = f"{integer_part}.{decimal_part[:2]}"
        e.control.value = value
        page.update()

    def validate_int(e):
        """
        Validates and formats the input as an integer, removing any non-digit characters.

        Args:
            e: The event triggered by changes in the text field.
        """
        e.control.value = ''.join(filter(str.isdigit, e.control.value))
        page.update()

    title = create_text_field("Title")
    cost = create_text_field("Cost", prefix_icon=ft.icons.EURO_SYMBOL, prefix_text="€", hint_text="0.00", validator=validate_float)
    quantity = create_text_field("Quantity", validator=validate_int)

    type_field = ft.Dropdown(
        label="Select Type",
        width=300,
        options=[ft.dropdown.Option(text=product['name'], key=product['id']) for product in get_products(uid, password)],
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_600,
        on_change=lambda e: update_register_button_state()
    )

    selected_file_path = None

    def on_image_selected(e):
        """
        Handles the image selection process. Validates the file type and updates
        the UI to indicate if a valid image was selected.

        Args:
            e: The event triggered by the file picker.
        """
        nonlocal selected_file_path
        if e.files:
            file_path = e.files[0].path
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                selected_file_path = file_path
                image_button.content.controls[1].content.value = "Photo Attached"
                image_button.style = ft.ButtonStyle(bgcolor=ft.colors.BLUE_GREY_400)
            else:
                selected_file_path = None
                show_snack_bar("Please select a valid image file (JPG, JPEG, PNG).")
        else:
            selected_file_path = None
            show_snack_bar("No image selected.")
        update_register_button_state()
        page.update()

    image_picker = ft.FilePicker(on_result=on_image_selected)
    page.overlay.append(image_picker)

    def create_button(text, icon, color, on_click, width=140, height=45):
        """
        Creates a styled button with an icon and specified functionality.

        Args:
            text (str): The label for the button.
            icon: The icon to display on the button.
            color: The background color of the button.
            on_click (function): Callback function to execute when the button is clicked.
            width (int): The width of the button. Defaults to 140.
            height (int): The height of the button. Defaults to 45.

        Returns:
            ft.ElevatedButton: A styled button component.
        """
        return ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(icon, color=ft.colors.WHITE, size=20),
                    ft.Container(
                        content=ft.Text(text, color=ft.colors.WHITE),
                        padding=ft.padding.only(right=10)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5,
            ),
            style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=color),
            on_click=on_click,
            width=width,
            height=height,
        )

    image_button = create_button("Attach Photo", ft.icons.ATTACH_FILE, ft.colors.BLUE_600, lambda _: image_picker.pick_files(allow_multiple=False))

    def show_snack_bar(message, is_error=True):
        """
        Displays a snack bar notification with a message.

        Args:
            message (str): The message to display in the snack bar.
            is_error (bool): Whether the message indicates an error. Defaults to True.
        """
        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            action="OK",
            action_color=ft.colors.BLUE_400,
            bgcolor=ft.colors.RED_700 if is_error else ft.colors.GREEN_700,
        )
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()

    def update_register_button_state():
        """
        Updates the state of the "Register" button based on whether all required
        fields have valid inputs.
        """
        register_button.disabled = not all([title.value, cost.value, quantity.value, type_field.value])
        register_button.style = ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.GREEN_600 if not register_button.disabled else ft.colors.GREY_400)
        page.update()

    def analyze_and_fill_fields():
        """
        Uses AI to analyze the attached invoice image and populate the relevant
        fields with extracted data. Handles errors and updates the UI accordingly.
        """
        if not selected_file_path:
            show_snack_bar("Please attach a photo first.")
            return

        loading_indicator.visible = True
        ia_button.disabled = True
        page.update()

        try:
            tipo_factura, titulo, precio_unitario, cantidad = analyze_invoice(selected_file_path, get_products(uid, password))
            title.value = titulo
            cost.value = str(precio_unitario)
            quantity.value = str(cantidad)
            type_field.value = tipo_factura
            update_register_button_state()
        except Exception as e:
            show_snack_bar(f"Error processing AI data: {str(e)}")
        finally:
            loading_indicator.visible = False
            ia_button.disabled = False
            page.update()

    def register_invoice(_):
        """
        Registers the invoice by sending the entered details and attached image
        to the server. Displays a success or error message based on the response.

        Args:
            _: The event triggered by the "Register" button click.
        """
        file_data = None
        if selected_file_path:
            with open(selected_file_path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')

        if send_data_invoice(uid, password, title.value, cost.value, quantity.value, type_field.value, file_data):
            show_snack_bar("Invoice registered successfully", is_error=False)
            go_back(_)
        else:
            show_snack_bar("Error registering invoice")

    register_button = create_button("Register", ft.icons.CHECK_CIRCLE, ft.colors.GREY_400, register_invoice, width=180)
    register_button.disabled = True

    loading_indicator = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2, color=ft.colors.BLUE_400)

    ia_button = create_button("AI Analysis", ft.icons.AUTO_AWESOME, ft.colors.PURPLE_600, lambda _: analyze_and_fill_fields())

    

    def go_back(_):
        """
        Navigates back to the main menu view.

        Args:
            _: The event triggered by the "Back" button click.
        """
        from .menu import menu_view
        page.clean()
        menu_view(page, uid, password, employee_id)
    back_button = create_button("Back", ft.icons.ARROW_BACK, ft.colors.BLUE_GREY_600, go_back, width=100)

    title_text = ft.Text("Register Invoice", size=24, weight=ft.FontWeight.BOLD)
    divider = ft.Divider(height=2)

    form_content = ft.Column([
        title_text,
        divider,
        type_field,
        title,
        cost,
        quantity,
        ft.Row([image_button, ia_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([back_button, register_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    form_container = ft.Container(
        content=form_content,
        width=360,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            offset=ft.Offset(0, 0),
        )
    )

    update_colors()  # Initial color setup
    theme_manager.add_listener(lambda _: update_colors())  # Listen for theme changes

    # Aplicar el tema guardado
    page.theme_mode = theme_manager.get_theme_mode()
    page.update()

    page.add(form_container)
    page.update()
    