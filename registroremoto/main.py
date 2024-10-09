import flet as ft

#El contenedor principal contiene el contenido de la pantalla
body = ft.Container(
    #Contenedor para distribuir los elementos horizontalmente
    ft.Row([
        ft.Container(
            ft.Column(controls=[
                # Muestra la imagen del logo la empresa Se utiliza un contenedor adicional para ajustar el padding
                ft.Container(ft.Image(src='logo.jpg', width=60, border_radius=50), alignment=ft.alignment.center),
                # Muestra el texto Iniciar Sesion
                ft.Text('Iniciar Sesión', width=360, size=25, weight='w900', text_align='center',),
                # Campo de texto para ingresar el correo electrónico
                ft.Container(ft.TextField(label='Correo electronico', suffix_text="@galvintec.com", width=280, height=40, color='black', prefix_icon=ft.icons.EMAIL,), alignment=ft.alignment.center),
                # Campo de texto para ingresar contraseña, el atributo password el estado True oculta el texto cuando se escribe
                ft.Container(ft.TextField(label='Contraseña', width=280, height=40, color='black', prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True), alignment=ft.alignment.center),
                # Un checkbox para recordar su contraseña.
                ft.Container(ft.Checkbox(label='Recordar contraseña', check_color='black', width=270), alignment=ft.alignment.center),
                # Un botón elevado para Iniciar.
                ft.Container(ft.ElevatedButton(content=ft.Text('INICIAR', color='white', weight='w500',), width=280, bgcolor='black',), alignment=ft.alignment.center),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY,),

            # Un degradado de color entre azul y rojo/rosa.
            gradient=ft.LinearGradient(['#27AFE3', '#EC4A6F']),
            # Ancho del contenedor
            width=325,
            # Altura del contenedor
            height=450,
            # El borde es redondeado con un radio de 20px.
            border_radius=20
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY,),
    padding=10,
)

def main(page: ft.Page):
    # Configuración de la ventana principal:
    page.window_width = 600
    page.window_height = 520
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.add(body)

ft.app(target=main)
