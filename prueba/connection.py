import xmlrpc.client

URL = "https://playground-odoo-14-prod.galvintec.dev/"
DB = "FCT2024Q4B"

class OdooConnection:
    """Clase para manejar la conexión con Odoo"""

    def authenticate(self, username, password):
        """Autenticar usuario en Odoo y devolver UID."""
        common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
        try:
            uid = common.authenticate(DB, username, password, {})
            print('UID:', uid)
            return uid
        
        except Exception as e:
            print("Error al autenticar el usuario:", e)
            return None

    def verificar_empleado_por_telefono(self, uid, password, phone_number):
        """Verifica si existe un empleado con el número de teléfono dado."""
        models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
        try:
            empleados = models.execute_kw(DB, uid, password,
                                          'hr.employee', 'search_read',
                                          [[['work_phone', '=', phone_number]]],  # Campo a verificar
                                          {'fields': ['id', 'name']})
            if empleados:
                return empleados[0]  # Devuelve el primer empleado encontrado
            else:
                return None
            
        except Exception as e:
            print("Error al buscar empleado por teléfono:", e)
            return None
