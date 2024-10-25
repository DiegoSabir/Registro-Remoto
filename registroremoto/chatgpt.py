"""Imports"""
# Standard Imports
import os

# Third Libraries
import openai
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

openai.api_key = os.getenv('API_CHATGPT')

