"""Imports"""
# Local Imports
import base64
import requests

# Third Imports
from app.credentials import CHATGPT_API_KEY

API_KEY = CHATGPT_API_KEY

def analyze_invoice(image_picker, products):
    """
    Analyzes an invoice or simplified invoice using GPT-based AI to extract 
    key details such as type of invoice, title, unit price, and quantity.

    Args:
        image_picker (str): Path to the image file of the invoice.
        products (list): List of products to classify the type of invoice.

    Returns:
        tuple: Contains the following extracted data:
            - tipo_factura (int): ID representing the type of invoice.
            - titulo (str): Title containing the name of the establishment 
              or service followed by the CIF (if available).
            - precio_unitario (float): Unit price formatted as a float.
            - cantidad (int): Quantity of the product.

    Raises:
        Exception: If there is an error in processing the AI response.
    """
    def encode_image_to_base64(image_path):
        """
        Encodes the image at the given path into a Base64 string for transmission.

        Args:
            image_path (str): Path to the image file to be encoded.

        Returns:
            str: Base64 encoded string of the image file.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    image_path = image_picker
    
    encoded_image = encode_image_to_base64(image_path)

    question = ("Analiza este documento, el cual puede ser una factura o una factura simplificada y obten, "
                "el tipo de factura, será uno de los elementos de esta lista (", products, ") , si no sabes cual decidir, usa el id 0 - expenses"
                "el titulo(su valor sera el nombre del establecimiento o servicio, seguido de un '-' y el CIF, en caso de no encontrar el CIF, deja esa parte en blanco), "
                "el precio por unidad(el valor será String pero con formato 0.00, no introduzcas caracteres no numéricos exceptuando el punto decimal), en caso de detectar varios productos distintos, el valor será el precio total de la factura, "
                "la cantidad de unidad(el valor será String pero con un numero, no introduzcas caracteres no numéricos), en caso de detectar varios productos distintos, el valor será 1.")

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
