import os
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

class Config:
    API_MODE: Literal["local", "online"] = os.getenv("API_MODE", "online")
    API_BASE_URL = (
        "http://127.0.0.1:11434/v1" 
        if API_MODE == "local" 
        else "https://api.deepseek.com/v1"
    )
    API_KEY = os.getenv("API_KEY", "a" if API_MODE == "local" else "")
    MODEL_NAME = (
        "deepseek-r1" 
        if API_MODE == "local" 
        else "deepseek-chat"
    )

config = Config()