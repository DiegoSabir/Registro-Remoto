"""IMPORTS"""

# Standard Imports
import os
from datetime import datetime

# Third Libraries
import xmlrpc.client
import dotenv

dotenv.load_dotenv()

# Get data for connection from env
URL = os.getenv('ODOO_URL')
DB = os.getenv('ODOO_DB')

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')



"""Login section"""



def authenticate(username, password):
    """
    Authenticate user in Odoo and get UID
    """
    try:
        uid = common.authenticate(DB, username, password, {})
        print('UID:', uid)
        return uid
    
    except Exception as e:
        print("Error al autenticar el usuario:", e)
        return None


def get_employee_id(uid, password):
    """
    asdasd
    """
    try:
        user = models.execute_kw(DB, uid, password, 
                                'res.users', 'read', [uid], 
                                {'fields': ['employee_id']})
        
        if user and 'employee_id' in user[0]:
            employee_id = user[0]['employee_id']
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

def get_attendance_records(uid, password):
    """
    asdasd
    """
    try:
        attendance_records = models.execute_kw(DB, uid, password,
                                            'hr.attendance', 'search_read', [[]], 
                                            {'fields': ['id', 'employee_id', 'check_in', 'check_out']})
        print("Registros de asistencia:")
        for record in attendance_records:
            print(record)

    except Exception as e:
        print("Error al obtener registros de asistencia:", e)
        

def list_employees(uid, password):
    """
    asdasd
    """
    employees = models.execute_kw(DB, uid, password,
                                'hr.employee', 'search_read', [[]], 
                                {'fields': ['id', 'name']})
    print("Empleados disponibles:")
    for employee in employees:
        print(employee)
        
"""
    Menu Section
"""

def get_user_name(uid, password, employee_uid):
    """
    asdasd
    """
    employee = models.execute_kw(DB, uid, password,
                                'hr.employee', 'search_read', 
                                [[['id', '=', employee_uid]]], 
                                {'fields': ['name'], 'limit': 1})
    if employee:
        return employee[0]['name']
    else:
        return "Empleado no encontrado."
    
    
def verify_assistance(uid, password, employee_id):
    """
    asdasd
    """
    if not isinstance(employee_id, int):
        try:
            employee_id = int(employee_id)

        except ValueError:
            print("Error: employee_id no es un número entero válido")
            return False

    try:
        attendance_records = models.execute_kw(DB, uid, password,
                                            'hr.attendance', 'search_read', 
                                            [[['employee_id', '=', employee_id], ['check_out', '=', False]]],
                                            {'fields': ['id']})
        return len(attendance_records) > 0  # Devuelve True si hay un registro activo
    
    except Exception as e:
        print("Error al verificar asistencia activa:", e)
        return False
    
def clock_in(uid, password, employee_id):
    """
    asdasd
    """
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attendance_id = models.execute_kw(DB, uid, password, 
                                        'hr.attendance', 'create', 
                                        [{'employee_id': employee_id, 'check_in': current_time}])
        print(f"Entrada registrada con éxito (ID: {attendance_id}).")
        return True
    
    except Exception as e:
        print("Error al fichar la entrada:", e)
        return False
    
def clock_out(uid, password, employee_id):
    """
    asdasd
    """
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # get present time
        # Search register of attendance
        attendance_records = models.execute_kw(DB, uid, password, 
                                            'hr.attendance', 'search_read', 
                                            [[['employee_id', '=', employee_id], ['check_out', '=', False]]],
                                            {'fields': ['id']})
        if attendance_records:
            attendance_id = attendance_records[0]['id']
            # Update attendance with check out time
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



def manage_check(uid, password, employee_id, tipo_fichaje, entrada_button, salida_button, page):
    """
    Manage the clock in or out from employee depending by type
    """
    if tipo_fichaje == 'entrada':
        if not verify_assistance(uid, password, employee_id):
            result = clock_in(uid, password, employee_id)
            if result: 
                entrada_button.visible = False  
                salida_button.visible = True
                print("Fichaje de entrada registrado exitosamente.")
            else:
                print("Error al fichar la entrada.")
        else:
            print("Ya has fichado la entrada, no puedes fichar de nuevo.")
    
    elif tipo_fichaje == 'salida':
        if verify_assistance(uid, password, employee_id):

            result = clock_out(uid, password, employee_id)
            if result: 
                salida_button.visible = False
                entrada_button.visible = True 
                print("Fichaje de salida registrado exitosamente.")
            else:
                print("Error al fichar la salida.")
        else:
            print("No puedes fichar la salida sin haber fichado la entrada.")
    
    else:
        print("Tipo de fichaje no válido.")
    
    # Update flet interface
    page.update()

"""
Diet Section
"""

def send_data_invoice(uid, password, descripcion, coste, cantidad, product_id, file_data=None):
    """
    ddddd
    """
    expense_data = {
        'name': descripcion,  
        'unit_amount': float(coste), 
        'quantity': int(cantidad),
        'product_id': int(product_id),  
    }

    try:
        expense_id = models.execute_kw(
            DB, uid, password, 
            'hr.expense', 'create', 
            [expense_data] 
        )
        print(f"Gasto registrado con ID: {expense_id}")

        # Si hay datos de imagen (file_data), adjuntar el archivo al gasto
        if file_data:
            attachment_data = {
                'name': "Gasto adjunto",  # Nombre del archivo
                'res_model': 'hr.expense',  # Modelo al que se adjunta
                'res_id': expense_id,  # ID del registro de gasto
                'type': 'binary',  # Tipo de archivo
                'datas': file_data,  # Imagen en base64
                'mimetype': 'image/jpeg',  # Tipo MIME de la imagen (ajustar según sea necesario)
            }

            attachment_id = models.execute_kw(
                DB, uid, password,
                'ir.attachment', 'create',
                [attachment_data]
            )
            print(f"Imagen adjunta con ID: {attachment_id}")

        return True
    except Exception as e:
        print(f"Error al registrar el gasto: {e}")
        return False
    

def get_products(uid, password):
    """
    knjdsjkndajknsdanjk
    """
    product_records = models.execute_kw(
        DB, uid, password,
        'product.product', 'search_read', 
        [[], ['name']],  
        {'limit': 50}  
    )

    # Extract products with his id and name
    products = [{'id': product['id'], 'name': product['name']} for product in product_records]
    return products