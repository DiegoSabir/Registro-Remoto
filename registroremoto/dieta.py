import flet as ft
from fondo import create_background_container  # Importar la función de fondo

def dieta_view(page: ft.Page):
    # Limpiar la página anterior
    page.clean()

    # Crear los campos de entrada con padding individual
    titulo_field = ft.Container(
        content=ft.TextField(label='Título de la factura', width=175, height=40),
        padding=ft.padding.all(10)
    )
    tipo_field = ft.Container(
        content=ft.Dropdown(
            label='Tipo de factura',
            options=[
                ft.dropdown.Option("Alojamiento"),
                ft.dropdown.Option("Alimentación"),
                ft.dropdown.Option("Transporte")
            ],
            width=175,
            height=40
        ),
        padding=ft.padding.all(10)
    )
    precio_field = ft.Container(
        content=ft.TextField(label='Precio', width=175, height=40),
        padding=ft.padding.all(10)
    )
    cantidad_field = ft.Container(
        content=ft.TextField(label='Cantidad', width=175, height=40),
        padding=ft.padding.all(10)
    )
    total_field = ft.Container(
        content=ft.TextField(label='Total', width=175, height=40, read_only=True),
        padding=ft.padding.all(10)
    )
    fecha_field = ft.Container(
        content=ft.TextField(label='Fecha', width=175, height=40),
        padding=ft.padding.all(10)
    )

    ia_button = ft.ElevatedButton(
        content=ft.Text('IA', color='white', weight='bold'),
        width=80,
        height=60,
        bgcolor='black',
        on_click=lambda e: None  # FUNCION PARA LA IA
    )

    # Función para actualizar el total automáticamente
    def actualizar_total(e):
        try:
            precio = float(precio_field.content.value)
            cantidad = int(cantidad_field.content.value)
            total = precio * cantidad
            total_field.content.value = str(total)
            page.update()
        except ValueError:
            total_field.content.value = "Error"
            page.update()

    # Asignar evento de cambio a los campos de precio y cantidad
    precio_field.content.on_change = actualizar_total
    cantidad_field.content.on_change = actualizar_total

    # Crear el diseño con más espacio entre los controles
    form_column = ft.Column(
        controls=[
            titulo_field,
            tipo_field,
            precio_field,
            cantidad_field,
            total_field,
            fecha_field
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=10
    )

    # Estructura del layout
    dieta_layout = ft.Row(
        controls=[form_column],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        spacing=40
    )

    # Añadir el botón de IA en la parte inferior con espacio
    dieta_content = ft.Column(
        controls=[
            dieta_layout,
            ft.Container(content=ia_button, alignment=ft.alignment.bottom_right, padding=ft.padding.only(right=20, bottom=10))
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        height=500
    )

    # Usar el fondo compartido para el contenedor principal
    body = create_background_container(content=dieta_content)

    # Agregar el contenido principal a la página
    page.add(body)

    # Actualizar la página al final
    page.update()
