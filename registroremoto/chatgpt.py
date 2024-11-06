"""

# Standard Imports
import os
#import openai
import dotenv
import openai

# Load environment variables from .env file
dotenv.load_dotenv()
openai.api_key = os.getenv('API_CHATGPT')

while True:
    prompt = input("\nIntroduce la pregunta:")

    completion = openai.Completion.create(engine="",
                                          prompt=prompt,
                                          max_tokens=2048)
    
    print(completion.choices[0].text)
"""