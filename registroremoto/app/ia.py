import json
import openai
import base64
import requests


#from utils.encrypt import decrypt_api

api_key=""

#api_key = decrypt_api() 

openai.api_key = api_key 

def analyze_allowance(image_picker, products):
    """
    Analyzes the image and returns processed data as variables.
    """
    def encode_image_to_base64(image_path):
        """
        Encodes image to base64 format.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Ruta de la imagen
    image_path = image_picker
    
    # Convertir la imagen a base64
    encoded_image = encode_image_to_base64(image_path)

    question = ("Analiza este documento, el cual puede ser una factura o una factura simplificada y obten, "
                "el tipo de factura, será el identificador de uno de los elementos de esta lista, si no sabe cual decidir, usa el id 0 - expenses (", products, ")"
                "el titulo(su valor sera el nombre del establecimiento o servicio), "
                "el precio por unidad(0.00), "
                "la cantidad de unidad(int), en caso de detectar distintos productos, coloca el precio total de unidad y de cantidad el valor sera 1.")

    rule_instructions = "Eres un asistente que extrae los datos especificos de facturas" 

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": f"{rule_instructions}."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{question}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                            "detail": "auto"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 120
    }

    # Hacer la solicitud a la API de OpenAI
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Convertir la respuesta JSON a un diccionario de Python
    response_dict = response.json()
    
    # Imprimir la respuesta cruda para depuración
    print("Raw JSON response:", json.dumps(response_dict, indent=4))  # Imprime el JSON formateado

    # Obtener el contenido del mensaje de la IA
    message_content = response_dict['choices'][0]['message']['content']

    # Procesar el contenido para extraer las variables
    tipo_factura, titulo, precio_unitario, cantidad = None, None, None, None

    # Procesar el contenido para extraer las variables
    lines = message_content.split("\n")
    for line in lines:
        if "Tipo de factura" in line:
            tipo_factura = int(line.split(":")[1].split("(")[0].strip())
        elif "Título" in line:
            titulo = line.split(":")[1].strip()
        elif "Precio por unidad" in line:
            precio_unitario = float(line.split(":")[1].strip())
        elif "Cantidad de unidad" in line:
            cantidad = int(line.split(":")[1].strip())
    
    print("ID de factura: ", tipo_factura,"Titulo: ",titulo, "Precio por unidad: ", precio_unitario, "Cantidad: ",cantidad)

    
    # Retornar las variables extraídas
    return tipo_factura, titulo, precio_unitario, cantidad