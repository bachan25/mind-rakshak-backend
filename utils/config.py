import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
MANAGEMENT_KEY = os.getenv("MANAGEMENT_KEY")