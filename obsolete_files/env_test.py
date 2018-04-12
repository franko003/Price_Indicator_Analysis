import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY = os.getenv('API_KEY')

print(API_KEY)
