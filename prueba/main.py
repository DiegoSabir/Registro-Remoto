import uuid
import flet
from flet import TextField, Column, ListTile, PopupMenuButton, PopupMenuItem, ElevatedButton, icons, Page, Text, Container, Image, Row, alignment, LinearGradient

import firebase_admin
from firebase_admin import firestore, credentials

from connection import OdooConnection

#cred = credentials.Certificate("C:/Users/desarrollo/Documents/GitHub/Registro-Remoto/prueba/serviceAccount.json")
cred = credentials.Certificate("C:/Users/diego/OneDrive/Documentos/GitHub/Registro-Remoto/prueba/serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class AppFire:
    """Clase para manejar la interfaz y la interacción con Firebase"""

    def __init__(self):
        self.phone_number = TextField(label="Teléfono", width=280, height=40, color='black')
        self.alldata = Column()
        self.odoo_conn = OdooConnection()


    def getdata(self):
        """Obtener todos los datos de Firebase"""

        docs = db.collection(u'users').stream()
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
            self.alldata.controls.append(
                ListTile(
                    title=Text(f"Teléfono: {str(doc.to_dict().get('phone_number', ''))}"),
                    trailing=PopupMenuButton(
                        icon=icons.MORE_VERT,
                        items=[PopupMenuItem(text="EDITAR"), PopupMenuItem(text="ELIMINAR")],
                    ),
                )
            )
        # Actualizar la interfaz después de cargar los datos
        self.alldata.update()



    def addnewdata(self, e):
        """Agregar datos a Firestore"""

        random_id = uuid.uuid1()
        user_ref = db.collection(u'users').document(str(random_id))
        try:
            user_ref.set({
                u'phone_number': self.phone_number.value,
            })
            self.alldata.controls.append(
                ListTile(
                    title=Text(f"Teléfono: {self.phone_number.value}"),
                    trailing=PopupMenuButton(
                        icon=icons.MORE_VERT,
                        items=[PopupMenuItem(text="EDITAR"), PopupMenuItem(text="ELIMINAR")],
                    ),
                )
            )
            # Actualizar la interfaz después de agregar nuevos datos
            self.alldata.update()
            
        except Exception as e:
            print("Error:", str(e))



    def verificar_numero(self, e):
        """Verificar número en Odoo y enviar código SMS si es válido"""
        phone_number = self.phone_number.value

        # Autenticación en Odoo
        uid = self.odoo_conn.authenticate('your_odoo_username', 'your_odoo_password')
        if uid:
            empleado = self.odoo_conn.verificar_empleado_por_telefono(uid, 'your_odoo_password', phone_number)
            if empleado:
                print(f"Empleado encontrado: {empleado['name']}. Enviando código SMS...")
            else:
                print("No se encontró ningún empleado con ese número de teléfono.")
        else:
            print("Error de autenticación en Odoo.")



    def build(self):
        """Construir la interfaz de usuario con colores y fondo"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Column(
                            controls=[
                                # Logo
                                Container(
                                    content=Image(src='logo.jpg', width=60, border_radius=50),
                                    alignment=alignment.center
                                ),
                                # Campo de entrada para el número de teléfono
                                Container(self.phone_number, alignment=alignment.center),
                                # Botón para verificar el número
                                Container(
                                    ElevatedButton(
                                        content=Text('Verificar Número', color='white', weight='w500'),
                                        width=280,
                                        bgcolor='black',
                                        on_click=self.verificar_numero  # Aquí está la función que verifica el número
                                    ),
                                    alignment=alignment.center
                                ),
                                # Lista de datos
                                self.alldata
                            ],
                            alignment="spaceEvenly"
                        ),
                        gradient=LinearGradient(
                            colors=['#27AFE3', '#EC4A6F'],
                        ),
                        width=325,
                        height=450,
                        border_radius=20,
                    )
                ],
                alignment="center"
            ),
            padding=10
        )

def main(page: Page):
    """Configuración de la ventana principal"""

    page.window.width = 600
    page.window.height = 520
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    
    # Instanciar la aplicación
    appfire = AppFire()
    # Añadir la vista principal a la página
    page.add(appfire.build())
    # Actualizar la página y cargar los datos
    page.update()
    appfire.getdata()

# Inicializar la aplicación
flet.app(target=main)