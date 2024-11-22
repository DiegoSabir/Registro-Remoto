"""Imports"""
# Local Imports
import base64
import requests

from app.credentials import CHATGPT_API_KEY

API_KEY = CHATGPT_API_KEY

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

    image_path = image_picker
    
    encoded_image = encode_image_to_base64(image_path)

    question = ("Analiza este documento, el cual puede ser una factura o una factura simplificada y obten, "
                "el tipo de factura, será uno de los elementos de esta lista, si no saber cual decidir, usa el id 0 - expenses (", products, ")"
                "el titulo(su valor sera el nombre del establecimiento o servicio), "
                "el precio por unidad(0.00), "
                "la cantidad de unidad(int), en caso de detectar distintos productos, coloca el precio total de unidad y de cantidad el valor sera 1.")

    rule_instructions = "Eres un asistente que extrae los datos especificos de facturas" 

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": f"{rule_instructions}."
            },
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
        "max_tokens": 100
    }

    # Make the request to the OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Convert JSON response to a Python dictionary
    response_dict = response.json()

    message_content = response_dict['choices'][0]['message']['content']

    # Process the content to extract the variables
    tipo_factura, titulo, precio_unitario, cantidad = None, None, None, None
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
    
    return tipo_factura, titulo, precio_unitario, cantidad
