""" Protocolo Llama a Procedimiento Remoto (RPC) """
import xmlrpc.client
from datetime import datetime

# Datos de la conexión
URL = "https://playground-odoo-14-prod.galvintec.dev/"
DB = "FCT2024Q4B"


def authenticate(username, password):
    """Autenticar usuario en Odoo y devolver UID."""

    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    try:
        uid = common.authenticate(DB, username, password, {})
        print('UID:', uid)
        return uid
    
    except Exception as e:
        print("Error al autenticar el usuario:", e)
        return None

def connect_models():
    """Conectar al objeto para acceder a modelos."""

    return xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

def obtener_nombre_usuario(uid, password, employee_uid):
    """uygfuytfug"""

    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    employee = models.execute_kw(DB, uid, password, 'hr.employee', 'search_read', [[['id', '=', employee_uid]]], {'fields': ['name'], 'limit': 1})
    if employee:
        return employee[0]['name']
    #else:
        #return "Empleado no encontrado."


def get_attendance_records(uid, password):
    """Obtener registros de asistencia."""

    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    try:
        attendance_records = models.execute_kw(DB, uid, password, 'hr.attendance', 'search_read', [[]], {'fields': ['id', 'employee_id', 'check_in', 'check_out']})
        print("Registros de asistencia:")
        for record in attendance_records:
            print(record)

    except Exception as e:
        print("Error al obtener registros de asistencia:", e)

def get_employee_id(uid, password):
    """Obtener el employee_id a partir del uid."""

    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')  
    try:
        user = models.execute_kw(DB, uid, password, 'res.users', 'read', [uid], {'fields': ['employee_id']})
        
        if user and 'employee_id' in user[0]:
            employee_id = user[0]['employee_id']
            
            # Si employee_id es una lista, tomar solo el ID (primer elemento)
            if isinstance(employee_id, list):
                employee_id = employee_id[0]

            print("Employee ID:", employee_id)
            return employee_id
        else:
            print("No se encontró el employee_id.")
            return None

    except Exception as e:
        print("Error al obtener el employee_id:", e)
        return None
    
    
def verificar_asistencia(uid, password, employee_id):
    """Verificar si hay un registro de asistencia activo para el empleado."""

    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    
    # Asegúrate de que employee_id es un número entero
    if not isinstance(employee_id, int):
        try:
            employee_id = int(employee_id)

        except ValueError:
            print("Error: employee_id no es un número entero válido")
            return False

    try:
        attendance_records = models.execute_kw(DB, uid, password, 'hr.attendance', 'search_read', [[['employee_id', '=', employee_id], ['check_out', '=', False]]], {'fields': ['id']})
        return len(attendance_records) > 0  # Devuelve True si hay un registro activo
    
    except Exception as e:
        print("Error al verificar asistencia activa:", e)
        return False
    
def fichar_entrada(uid, password, employee_id):
    """Registrar la entrada del empleado."""

    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attendance_id = models.execute_kw(DB, uid, password, 'hr.attendance', 'create', [{'employee_id': employee_id, 'check_in': current_time}])
        print(f"Entrada registrada con éxito (ID: {attendance_id}).")
        return True
    
    except Exception as e:
        print("Error al fichar la entrada:", e)
        return False
    
def fichar_salida(uid, password, employee_id):
    """Registrar la salida del empleado en el módulo de asistencias."""

    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtener la hora actual
        # Buscar el registro de asistencia activo
        attendance_records = models.execute_kw(DB, uid, password, 
                                            'hr.attendance', 'search_read', 
                                            [[['employee_id', '=', employee_id], ['check_out', '=', False]]],
                                            {'fields': ['id']})
        if attendance_records:
            attendance_id = attendance_records[0]['id']
            # Actualizar el registro de asistencia con la hora de salida
            models.execute_kw(DB, uid, password, 
                            'hr.attendance', 'write', 
                            [[attendance_id], {'check_out': current_time}])
            print(f"Salida registrada exitosamente para ID: {attendance_id}")
            return True
        else:
            print("No se encontró un registro de entrada para este empleado.")
            return False
        
    except Exception as e:
        print("Error al registrar la salida:", e)
        return False

def gestionar_fichaje(uid, password, employee_id, tipo_fichaje, entrada_button, salida_button, page):
    """Gestionar el fichaje (entrada o salida) del empleado según el tipo."""
    
    # Verificar si el usuario ya ha fichado
    if tipo_fichaje == 'entrada':
        if not verificar_asistencia(uid, password, employee_id):
            # Realizar el fichaje de entrada
            resultado = fichar_entrada(uid, password, employee_id)
            if resultado:  # Suponiendo que fichar_entrada retorna True en caso de éxito
                entrada_button.visible = False  # Ocultar botón de entrada
                salida_button.visible = True  # Mostrar botón de salida
                print("Fichaje de entrada registrado exitosamente.")
            else:
                print("Error al fichar la entrada.")
        else:
            print("Ya has fichado la entrada, no puedes fichar de nuevo.")
    
    elif tipo_fichaje == 'salida':
        if verificar_asistencia(uid, password, employee_id):
            # Realizar el fichaje de salida
            resultado = fichar_salida(uid, password, employee_id)
            if resultado:  # Suponiendo que fichar_salida retorna True en caso de éxito
                salida_button.visible = False  # Ocultar botón de salida
                entrada_button.visible = True  # Mostrar botón de entrada
                print("Fichaje de salida registrado exitosamente.")
            else:
                print("Error al fichar la salida.")
        else:
            print("No puedes fichar la salida sin haber fichado la entrada.")
    
    else:
        print("Tipo de fichaje no válido.")
    
    # Actualizar la página una sola vez al final
    page.update()
