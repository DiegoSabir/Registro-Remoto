import flet as ft
from fondo import create_background_container  # Importar la función de fondo

def dieta_view(page: ft.Page):
    # Limpiar la página anterior
    page.clean()

    # Crear los campos de entrada
    titulo_field = ft.TextField(label='Título de la factura', width=280, height=40)
    tipo_field = ft.Dropdown(
        label='Tipo de factura',
        options=[
            ft.dropdown.Option("Alojamiento"),
            ft.dropdown.Option("Alimentación"),
            ft.dropdown.Option("Transporte")
        ],
        width=280,
        height=40
    )
    precio_field = ft.TextField(label='Precio', width=280, height=40)
    cantidad_field = ft.TextField(label='Cantidad', width=280, height=40)
    total_field = ft.TextField(label='Total', width=280, height=40, read_only=True)
    fecha_field = ft.TextField(label='Fecha', width=280, height=40)
    imagen_field = ft.TextField(label='Adjuntar Imagen', width=280, height=40)

    # Botón para la IA (por ahora no hace nada)
    ia_button = ft.ElevatedButton(
        content=ft.Text('IA', color='white', weight='bold'),
        width=60,
        height=60,
        bgcolor='black',
        border_radius=30,
        on_click=lambda e: None  # FUNCION PARA LA IA
    )

    # Función para actualizar el total automáticamente
    def actualizar_total(e):
        try:
            precio = float(precio_field.value)
            cantidad = int(cantidad_field.value)
            total = precio * cantidad
            total_field.value = str(total)
            page.update()
        except ValueError:
            total_field.value = "Error"
            page.update()

    # Asignar evento de cambio a los campos de precio y cantidad
    precio_field.on_change = actualizar_total
    cantidad_field.on_change = actualizar_total

    # Crear el diseño basado en la imagen proporcionada
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

    # Contenedor para la imagen
    image_container = ft.Container(
        content=ft.Text('Imagen', size=18, weight='bold'),
        width=150,
        height=200,
        border=ft.border.all(2, 'black'),
        alignment=ft.alignment.center
    )

    # Estructura del layout
    dieta_layout = ft.Row(
        controls=[
            form_column,
            image_container,
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        spacing=20
    )

    # Añadir el botón de IA en la parte inferior
    dieta_content = ft.Column(
        controls=[
            dieta_layout,
            ft.Container(content=ia_button, alignment=ft.alignment.bottom_right)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        height=500  # Ajustar la altura para que quepan todos los elementos
    )

    # Usar el fondo compartido para el contenedor principal
    body = create_background_container(content=dieta_content)

    # Agregar el contenido principal a la página
    page.add(body)

    # Actualizar la página al final
    page.update()
