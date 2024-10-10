# Protocolo Llama a Procedimiento Remoto (RPC)
import xmlrpc.client

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

def get_version():
    """Obtener la versión del servidor Odoo."""
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    try:
        version_info = common.version()
        print("Versión de Odoo:", version_info)

    except Exception as e:
        print("Error al obtener la versión:", e)

def connect_models():
    """Conectar al objeto para acceder a modelos."""
    return xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

def list_employees(models, uid, password):
    """Listar empleados en el sistema."""
    employees = models.execute_kw(DB, uid, password,
                                'hr.employee', 'search_read', [[]], 
                                {'fields': ['id', 'name']})
    print("Empleados disponibles:")
    for employee in employees:
        print(employee)

def get_attendance_records(models, uid, password):
    """Obtener registros de asistencia."""
    try:
        attendance_records = models.execute_kw(DB, uid, password,
                                            'hr.attendance', 'search_read', [[]], 
                                            {'fields': ['id', 'employee_id', 'check_in', 'check_out']})
        print("Registros de asistencia:")
        for record in attendance_records:
            print(record)

    except Exception as e:
        print("Error al obtener registros de asistencia:", e)

def get_employee_id(models, uid, password):
    """Obtener el employee_id a partir del uid."""
    try:
        user = models.execute_kw(DB, uid, password,
                                'res.users', 'read', [uid], 
                                {'fields': ['employee_id']})

        employee_id = user[0]['employee_id'] if user else None
        print("Employee ID:", employee_id)
        return employee_id
    
    except Exception as e:
        print("Error al obtener el employee_id:", e)
        return None
    
    