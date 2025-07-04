from google import genai
from pydantic import BaseModel
from file_tools import *
from image_generator import *
from use_cli import *

with open("api_key.txt", "r") as f:
    api_key = f.read().strip()

client = genai.Client(api_key=api_key)
chat = client.chats.create(model="gemini-2.5-flash",
                           contents="")




