from pymongo import MongoClient
from dotenv import load_dotenv
from decouple import config
import regex as re
import bcrypt, os

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

mongo_url = 'mongodb://localhost:27017/'
client = MongoClient(mongo_url)
db = client["users_database"]
users_collection = db["users"]

def validate_username(username):
    pattern = r"[a-z0-9_]{3, 20}$"
    if re.match(pattern, username):
        return True, "Valid username."
    return False, "Invalid username."

def validate_email(email):
    pattern = r"[a-zA-Z0-9._]"
    
# def sign_up(username, email, password):
    
    