import base64
import flet as ft
from utils.connection import send_data_invoice, get_products
from .ia import analyze_allowance


def allowance_view(page: ft.Page, uid, password, employee_id):
    page.clean()
    page.bgcolor = ft.colors.BLUE_50
    page.padding = 20
    page.window_width = 400
    page.window_height = 700
    page.window_resizable = False
    page.title = "Galvintec Allowance Registration"

    def create_text_field(label, width=300, prefix_icon=None, prefix_text=None, hint_text=None, validator=None):
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
        try:
            float_val = float(e.control.value)
            e.control.value = f"{float_val:.2f}"
        except ValueError:
            e.control.value = ""
        page.update()

    def validate_int(e):
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
    )

    selected_file_path = None

    def on_image_selected(e):
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
        register_button.disabled = not all([title.value, cost.value, quantity.value, type_field.value])
        register_button.style = ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.GREEN_600 if not register_button.disabled else ft.colors.GREY_400)
        page.update()

    def analyze_and_fill_fields():
        if not selected_file_path:
            show_snack_bar("Please attach a photo first.")
            return

        loading_indicator.visible = True
        ia_button.disabled = True
        page.update()

        try:
            tipo_factura, titulo, precio_unitario, cantidad = analyze_allowance(selected_file_path, get_products(uid, password))
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

    def register_allowance(_):
        file_data = None
        if selected_file_path:
            with open(selected_file_path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')

        if send_data_invoice(uid, password, title.value, cost.value, quantity.value, type_field.value, file_data):
            show_snack_bar("Allowance registered successfully", is_error=False)
            go_back(_)
        else:
            show_snack_bar("Error registering allowance")

    register_button = create_button("Register", ft.icons.CHECK_CIRCLE, ft.colors.GREY_400, register_allowance, width=180)
    register_button.disabled = True

    loading_indicator = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2, color=ft.colors.BLUE_400)

    ia_button = create_button("AI Analysis", ft.icons.AUTO_AWESOME, ft.colors.PURPLE_600, lambda _: analyze_and_fill_fields())

    from .menu import menu_view

    def go_back(_):
        page.clean()
        menu_view(page, uid, password, employee_id)

    back_button = create_button("Back", ft.icons.ARROW_BACK, ft.colors.BLUE_GREY_600, go_back, width=100)

    form_content = ft.Column([
        ft.Text("Register Allowance", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
        ft.Divider(height=2, color=ft.colors.BLUE_200),
        type_field,
        title,
        cost,
        quantity,
        ft.Row([image_button, ia_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([back_button, register_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    page.add(
        ft.Container(
            content=form_content,
            width=360,
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
            )
        )
    )
    page.update()

# For demonstration purposes
if __name__ == "__main__":
    def main(page: ft.Page):
        allowance_view(page, "dummy_uid", "dummy_password", "dummy_employee_id")

    ft.app(target=main)