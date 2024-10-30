"""IMPORTS"""

# Standard Imports
import os
from datetime import datetime, timezone

# Third Libraries
import xmlrpc.client
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Get data for connection from env
URL = os.getenv('ODOO_URL')
DB = os.getenv('ODOO_DB')

# Get xmlrpc directions for all the query
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# Timezone set
#TIMEZONE = pytz.timezone('Europe/Madrid')


########################################### Login section ##########################################


def authenticate(username, password):
    """
    Authenticate the user with Odoo and retrieve the user ID (UID).

    :param username (str): The user's username.
    :param password (str): The user's password.

    
    return: int: The user ID if authentication is successful, otherwise None.
    """
    try:
        uid = common.authenticate(DB, username, password, {})
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        print("Hora actual:", current_time)
        print('UID:', uid)
        return uid
    
    except Exception as e:
        print("Error during user authentication:", e)
        return None


def get_employee_id(uid, password):
    """
    Retrieve the employee ID associated with the authenticated user.

    :param uid (int): The user ID.
    :param password (str): The user's password.

    :return int: The employee ID if found, otherwise None.
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
        #else:
        #    print("No se encontró el employee_id.")
        #    return None

    except Exception as e:
        print("Error retrieving employee ID:", e)
        return None

def get_attendance_records(uid, password):
    """
    Retrieve and display attendance records for all users.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    """
    try:
        attendance_records = models.execute_kw(DB, uid, password,
                                               'hr.attendance', 'search_read', [[]],
                                               {'fields': ['id', 'employee_id', 'check_in', 'check_out']})
        print("Attendance Records:")
        for record in attendance_records:
            print(record)

    except Exception as e:
        print("Error retrieving attendance records:", e)
        
def list_employees(uid, password):
    """
    List all employees.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    """
    employees = models.execute_kw(DB, uid, password,
                                  'hr.employee', 'search_read', [[]],
                                  {'fields': ['id', 'name']})
    print("Available Employees:")
    for employee in employees:
        print(employee)



################################################# Menu Section ####################################################



def get_user_name(uid, password, employee_uid):
    """
    Retrieve the name of the user.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param employee_uid (int): The employee ID.

    :return str: The name of the employee, or an error message if not found.
    """
    employee = models.execute_kw(DB, uid, password,
                                 'hr.employee', 'search_read', [[['id', '=', employee_uid]]],
                                 {'fields': ['name'], 'limit': 1})
    if employee:
        return employee[0]['name']
    else:
        return "Empleado no encontrado."
        

def verify_assistance(uid, password, employee_id):
    """
    Check if the employee is currently checked in.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param employee_id (int): The employee ID.

    :return bool: True if the employee has an active attendance record, False otherwise.
    """
    if not isinstance(employee_id, int):
        try:
            employee_id = int(employee_id)

        except ValueError:
            print("Error: is not a valid integer")
            return False

    try:
        attendance_records = models.execute_kw(DB, uid, password,
                                               'hr.attendance', 'search_read', [[['employee_id', '=', employee_id],
                                               ['check_out', '=', False]]], {'fields': ['id']})
        return len(attendance_records) > 0  
    
    except Exception as e:
        print("Error checking active attendance:", e)
        return False

def clock_in(uid, password, employee_id):
    """
    Clock in for an employee.
    """
    try:
        # Obtener la hora actual en UTC
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        attendance_id = models.execute_kw(DB, uid, password,
                                          'hr.attendance', 'create',
                                          [{'employee_id': employee_id, 'check_in': current_time}])
        print(f"Clock-in successful (ID: {attendance_id}).")
        return True

    except Exception as e:
        print("Error clocking in:", e)
        return False

def clock_out(uid, password, employee_id):
    """
    Clock out for an employee.
    """
    try:
        # Obtener la hora actual en UTC
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        attendance_records = models.execute_kw(DB, uid, password,
                                               'hr.attendance', 'search_read',
                                               [[['employee_id', '=', employee_id], ['check_out', '=', False]]], {'fields': ['id']})
        if attendance_records:
            attendance_id = attendance_records[0]['id']
            models.execute_kw(DB, uid, password, 'hr.attendance', 'write', [[attendance_id], {'check_out': current_time}])
            print(f"Clock-out successful for ID: {attendance_id}")
            return True

    except Exception as e:
        print("Error clocking out:", e)
        return False

def manage_check(uid, password, employee_id, tipo_fichaje, clock_in_button, clock_out_button, page):
    """
    Manage the clock-in or clock-out process for an employee based on the type.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param employee_id (int): The employee ID.
    :param tipo_fichaje (str): The type of clock action ('entrada' or 'salida').
    :param clock_in_button (ft.Button): The button used for clocking in.
    :param clock_out_button (ft.Button): The button used for clocking out.
    :param page (ft.Page): The current page being displayed in the interface.
    """
    if tipo_fichaje == 'enter':
        if not verify_assistance(uid, password, employee_id):
            result = clock_in(uid, password, employee_id)
            if result: 
                clock_in_button.visible = False  
                clock_out_button.visible = True
                print("Clock-in recorded successfully.")
            else:
                print("Error clocking in.")

    elif tipo_fichaje == 'exit':
        if verify_assistance(uid, password, employee_id):
            result = clock_out(uid, password, employee_id)
            if result:
                clock_out_button.visible = False
                clock_in_button.visible = True 
                print("Clock-out recorded successfully.")
            else:
                print("Error clocking out.")

    # Update flet interface
    page.update()



############################################ Allowance Section #####################################



def send_data_invoice(uid, password, description, cost, quantity, product_id, file_data=None):
    """
    Register an expense in Odoo.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param description (str): The description of the expense.
    :param cost (float): The unit cost of the expense.
    :param quantity (int): The quantity of the expense.
    :param product_id (int): The ID of the product associated with the expense.
    :param file_data (str, optional): Base64 encoded image data for an attachment.

    return: bool: True if the expense was registered successfully, otherwise False.
    """
    expense_data = {
        'name': description,  
        'unit_amount': float(cost), 
        'quantity': int(quantity),
        'product_id': int(product_id),  
    }

    try:
        expense_id = models.execute_kw(DB, uid, password,
                                       'hr.expense', 'create',
                                       [expense_data] )
        print(f"Expense registered with ID: {expense_id}")

        # If there are images (file_data), attach it to the allowance register
        if file_data:
            attachment_data = {
                'name': "Gasto adjunto",  # Name of the register
                'res_model': 'hr.expense',  # Objective module
                'res_id': expense_id,  # ID of expense register
                'type': 'binary',  # type of file
                'datas': file_data,  # Image in base64
                'mimetype': 'image/jpeg',  # Tipo MIME de la imagen (ajustar según sea necesario)
            }
            attachment_id = models.execute_kw(DB, uid, password,
                                              'ir.attachment', 'create',
                                              [attachment_data])
            print(f"Imagen adjunta con ID: {attachment_id}")
        return True
    
    except Exception as e:
        print(f"Error registering the expense: {e}")
        return False
    

def get_products(uid, password):
    """
    Retrieve a list of products from Odoo.

    :param uid (int): The user ID.
    :param password (str): The user's password.

    :return list: A list of dictionaries containing product ID and name.
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