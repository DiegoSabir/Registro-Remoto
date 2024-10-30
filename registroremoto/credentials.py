"""Imports"""

# Standard Imports
import os

# Third Libraries
from dotenv import load_dotenv

def update_env_variable(key, value, env_file='.env'):
    """
    Update an environment variable in the specified .env file.

    :param key (str): The name of the environment variable to update.
    :param value (str): The new value for the environment variable.
    :param env_file (str, optional): The path to the .env file. Defaults to '.env'.
    
    return: None
    """
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    else:
        lines = []

    key_exists = False
    with open(env_file, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.startswith(f"{key}="):
                file.write(f"{key}={value}\n")
                key_exists = True
            else:
                file.write(line)

        if not key_exists:
            file.write(f"{key}={value}\n")
    
    print(f"'{key}' actualizado o añadido en {env_file}")
