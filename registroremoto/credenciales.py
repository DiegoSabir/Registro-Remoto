import os
from dotenv import load_dotenv

def update_env_variable(key, value, env_file='.env'):
    """Actualizar una variable en el archivo .env"""
    
    # Leer el archivo .env si existe
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            lines = file.readlines()
    else:
        lines = []

    # Ver si la clave ya existe y necesita actualización
    key_exists = False
    with open(env_file, 'w') as file:
        for line in lines:
            if line.startswith(f"{key}="):
                # Actualiza el valor de la clave
                file.write(f"{key}={value}\n")
                key_exists = True
            else:
                file.write(line)

        # Si la clave no existía, agregarla al final
        if not key_exists:
            file.write(f"{key}={value}\n")
    
    print(f"'{key}' actualizado o añadido en {env_file}")