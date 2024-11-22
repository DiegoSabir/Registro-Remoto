"""IMPORTS"""

# Standard Imports
from datetime import datetime, timezone

# Third Libraries
import xmlrpc.client
import flet as ft

common = None
models = None
db_stored = None

########################################### Sign In Section ##########################################

def setup_connection(url, db):
    """
    Sets up the connection to the Odoo server using XML-RPC.

    :param url (str): The URL of the Odoo server.
    :param db (str): The name of the database to connect to.
    
    :return bool: True if the connection was successfully established, False otherwise.
    """
    global common, models, db_stored
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', allow_none=True)
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', allow_none=True)
        db_stored = db
        print("Conexión configurada correctamente.")
        return True
    
    except Exception as e:
        print(f"Error al configurar la conexión: {e}")
        return False

def authenticate(email, password, url, db):
    """
    Authenticates the user on the Odoo server using XML-RPC.

    :param email (str): The user's email.
    :param password (str): The user's password.
    :param url (str): The URL of the Odoo server.
    :param db (str): The database name.
    
    :return int: The user ID if authentication is successful, None otherwise.
    """
    try:
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        uid = common.authenticate(db, email, password, {})
        return uid
    
    except Exception as e:
        print(f"Error en la autenticación: {e}")
        return None

def get_employee_id(uid, password, url, db):
    """
    Retrieves the employee ID for the authenticated user.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param url (str): The URL of the Odoo server.
    :param db (str): The database name.
    
    :return int: The employee ID if found, None otherwise.
    """
    try:
        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'search', [[['user_id', '=', uid]]])
        return employee_id[0] if employee_id else None
    
    except Exception as e:
        print(f"Error obteniendo el ID del empleado: {e}")
        return None
    
def get_attendance_records(uid, password):
    """
    Retrieve and display attendance records for all users.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    """
    try:
        attendance_records = models.execute_kw(db_stored, uid, password,
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
    employees = models.execute_kw(db_stored, uid, password,
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
    employee = models.execute_kw(db_stored, uid, password,
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
        attendance_records = models.execute_kw(db_stored, uid, password,
                                            'hr.attendance', 'search_read', [[['employee_id', '=', employee_id],
                                            ['check_out', '=', False]]], {'fields': ['id']})
        return len(attendance_records) > 0  
    
    except Exception as e:
        print("Error checking active attendance:", e)
        return False

def clock_in(uid, password, employee_id):
    """
    Registers a clock-in for an employee.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param employee_id (int): The employee ID.
    
    :return bool: True if the clock-in was successful, False otherwise.
    """
    try:
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        attendance_id = models.execute_kw(db_stored, uid, password,
                                        'hr.attendance', 'create',
                                        [{'employee_id': employee_id, 'check_in': current_time}])
        print(f"Clock-in successful (ID: {attendance_id}).")
        return True

    except Exception as e:
        print("Error clocking in:", e)
        return False

def clock_out(uid, password, employee_id):
    """
    Registers a clock-out for an employee.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param employee_id (int): The employee ID.
    
    :return bool: True if the clock-out was successful, False otherwise.
    """
    try:
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        attendance_records = models.execute_kw(db_stored, uid, password,
                                            'hr.attendance', 'search_read',
                                            [[['employee_id', '=', employee_id], ['check_out', '=', False]]], {'fields': ['id']})
        if attendance_records:
            attendance_id = attendance_records[0]['id']
            models.execute_kw(db_stored, uid, password, 'hr.attendance', 'write', [[attendance_id], {'check_out': current_time}])
            print(f"Clock-out successful for ID: {attendance_id}")
            return True

    except Exception as e:
        print("Error clocking out:", e)
        return False

def show_popup(page, message):
    """
    Creates and displays a popup with the error message.

    :param page (ft.Page): The current Flet page.
    :param message (str): The message to display in the popup.
    """
    popup_dialog = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("OK", on_click=lambda e: close_popup(page, popup_dialog))
        ]
    )
    page.dialog = popup_dialog
    popup_dialog.open = True
    page.update()

def close_popup(page, dialog):
    """
    Closes the popup dialog.

    :param page (ft.Page): The current Flet page.
    :param dialog (ft.AlertDialog): The dialog to close.
    """
    dialog.open = False
    page.update()

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
                show_popup(page, "Error clocking in.")
        else:
            show_popup(page, "You are already clocked in on another device.")
            clock_in_button.visible = False
            clock_out_button.visible = True

    elif tipo_fichaje == 'exit':
        if verify_assistance(uid, password, employee_id):
            result = clock_out(uid, password, employee_id)
            if result:
                clock_out_button.visible = False
                clock_in_button.visible = True
                print("Clock-out recorded successfully.")
            else:
                show_popup(page, "Error clocking out.")
        else:
            show_popup(page, "You are not clocked in on this device.")
            clock_out_button.visible = False
            clock_in_button.visible = True

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
        expense_id = models.execute_kw(db_stored, uid, password,
                                    'hr.expense', 'create',
                                    [expense_data] )

        if file_data:
            attachment_data = {
                'name': "Gasto adjunto",
                'res_model': 'hr.expense',
                'res_id': expense_id,
                'type': 'binary',
                'datas': file_data,
                'mimetype': 'image/jpeg',
            }
            attachment_id = models.execute_kw(db_stored, uid, password,
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
        db_stored, uid, password,
        'product.product', 'search_read',
        [[], ['name']],
        {'limit': 50}
    )

    products = [{'id': product['id'], 'name': product['name']} for product in product_records]
    return products