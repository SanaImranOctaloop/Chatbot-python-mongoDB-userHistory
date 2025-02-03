from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
    MONGODB_URI = os.getenv("MONGODB_URI")
    if not MONGODB_URI:
        raise Exception("MONGODB_URI is not set in the .env file")
    #client = MongoClient(MONGODB_URI)
    return MongoClient(MONGODB_URI)['chatbot']
