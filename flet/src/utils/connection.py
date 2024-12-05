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
    Check if the employee is currently checked in and retrieve the check-in time.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param employee_id (int): The employee ID.

    :return tuple: (bool, str) A tuple where the first value indicates if the employee is checked in, and the second is the check-in time (or None if not found).
    """
    if not isinstance(employee_id, int):
        try:
            employee_id = int(employee_id)
        except ValueError:
            print("Error: Employee ID is not a valid integer")
            return False, None

    try:
        attendance_records = models.execute_kw(
            db_stored, uid, password,
            'hr.attendance', 'search_read',
            [[['employee_id', '=', employee_id], ['check_out', '=', False]]],
            {'fields': ['id', 'check_in']}
        )
        if attendance_records:
            check_in_time = attendance_records[0].get('check_in')
            
            return True, check_in_time
        return False, None
    except Exception as e:
        print("Error checking active attendance:", e)
        return False, None

def update_work_hours(uid, password, employee_id, check_in_text, page):
    """
    Updates the total working hours for the day based on clock-in and clock-out times.
    
    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param employee_id (int): The employee ID.
    :param check_in_text (ft.Text): The text widget to display the total worked hours.
    """
    try:
        # Get today's date in YYYY-MM-DD format
        today_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        # Fetch attendance records for today
        attendance_records = models.execute_kw(
            db_stored, uid, password,
            'hr.attendance', 'search_read',
            [[['employee_id', '=', employee_id], 
              ['check_in', '>=', today_date + ' 00:00:00'],
              ['check_in', '<=', today_date + ' 23:59:59']]],  # Fetch only today's records
            {'fields': ['check_in', 'check_out']}
        )
        

        total_worked_seconds = 0
        now_time = datetime.now(timezone.utc)  # Get the current UTC time

        for record in attendance_records:
            # Convert check_in to datetime and ensure it is timezone-aware (UTC)
            check_in_time = datetime.strptime(record['check_in'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
            
            if record['check_out']:
                # If check_out exists, calculate time between check_in and check_out
                check_out_time = datetime.strptime(record['check_out'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                worked_time = check_out_time - check_in_time
            else:
                # If check_out is missing, calculate time between check_in and now
                worked_time = now_time - check_in_time
            
            total_worked_seconds += worked_time.total_seconds()

        # Convert total worked time in seconds to hours and minutes
        worked_hours = int(total_worked_seconds // 3600)  # Convert to integer
        worked_minutes = int((total_worked_seconds % 3600) // 60)  # Convert to integer
        
        # Debugging: Check worked hours and minutes
        print(f"Worked hours: {worked_hours}, Worked minutes: {worked_minutes}")

        # Update the check_in_text to show the total worked hours
        if total_worked_seconds > 0:
            check_in_text.value = f"Total worked today: {worked_hours} hours {worked_minutes} minutes"
        else:
            check_in_text.value = "No work hours recorded for today."
        
        check_in_text.visible = True

    except Exception as e:
        print(f"Error calculating work hours: {e}")
        check_in_text.value = "Error calculating work hours."
        check_in_text.visible = True

    # Update the page to reflect changes
    page.update()

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

def manage_check(uid, password, employee_id, tipo_fichaje, clock_in_button, clock_out_button, page, check_in_text):
    """
    Manage the clock-in or clock-out process for an employee based on the type.

    :param uid (int): The user ID.
    :param password (str): The user's password.
    :param employee_id (int): The employee ID.
    :param tipo_fichaje (str): The type of clock action ('enter' or 'exit').
    :param clock_in_button (ft.Button): The button used for clocking in.
    :param clock_out_button (ft.Button): The button used for clocking out.
    :param page (ft.Page): The current page being displayed in the interface.
    :param check_in_text (ft.Text): The text widget displaying the clock-in time.
    """
    if tipo_fichaje == 'enter':
        is_checked_in, check_in_time = verify_assistance(uid, password, employee_id)
        if not is_checked_in:
            result = clock_in(uid, password, employee_id)
            if result:
                clock_in_button.visible = False
                clock_out_button.visible = True
                print("Clock-in recorded successfully.")

                update_work_hours(uid, password, employee_id, check_in_text, page)
            else:
                show_popup(page, "Error clocking in.")
        else:
            show_popup(page, "You are already clocked in on another device.")
            clock_in_button.visible = False
            clock_out_button.visible = True

    elif tipo_fichaje == 'exit':
        is_checked_in, _ = verify_assistance(uid, password, employee_id)
        if is_checked_in:
            result = clock_out(uid, password, employee_id)
            if result:
                clock_out_button.visible = False
                clock_in_button.visible = True
                update_work_hours(uid, password, employee_id, check_in_text, page)
                print("Clock-out recorded successfully.")
                
                # Hide the clock-in time
                check_in_text.value = ""
                check_in_text.visible = False
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



############################################ ALlowance List Section #####################################



def get_employee_expenses(uid, password):
    """
    Obtener los gastos registrados por el empleado.

    :param uid (int): El ID del usuario.
    :param password (str): La contraseña del usuario.
    
    :return: List of expenses registered by the employee.
    """
    try:
        # Primero obtener el ID del empleado del usuario actual
        employee_id = models.execute_kw(db_stored, uid, password, 
                                        'hr.employee', 'search',
                                        [[['user_id', '=', uid]]])  # Filtramos por el usuario
        
        if not employee_id:
            print("Empleado no encontrado.")
            return []

        # Ahora obtenemos los gastos relacionados con este empleado
        expenses = models.execute_kw(db_stored, uid, password, 
                                    'hr.expense', 'search_read',
                                    [[['employee_id', '=', employee_id[0]]]], 
                                    {'fields': ['name', 'unit_amount', 'quantity', 'product_id', 'date', 'state']})

        return expenses
    
    except Exception as e:
        print(f"Error fetching expenses: {e}")
        return []
    
def delete_expense(uid, password, expense_id, page):
    """
    Eliminar un gasto registrado por el empleado.

    :param uid (int): El ID del usuario.
    :param password (str): La contraseña del usuario.
    :param expense_id (int): El ID del gasto a eliminar.
    
    :return: True si se eliminó el gasto, False si hubo un error.
    """
    try:
        # Eliminar el gasto
        models.execute_kw(db_stored, uid, password, 
                        'hr.expense', 'unlink', 
                        [[expense_id]])
        print(f"Gasto con ID {expense_id} eliminado.")
        page.update()
        return True
    
    except Exception as e:
        print(f"Error eliminando el gasto: {e}")
        return False
