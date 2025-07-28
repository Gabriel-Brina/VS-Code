from dotenv import load_dotenv
import os

load_dotenv()

CLINT_API_URL = os.getenv("CLINT_API_URL")
CLINT_TOKEN = os.getenv("CLINT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")