import os
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
token = os.environ.get("token")
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")