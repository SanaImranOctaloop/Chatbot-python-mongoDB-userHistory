from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
    connection_string = os.getenv("MONGODB_URI")
    if not connection_string:
        raise Exception("MONGODB_URI is not set in the .env file")
    #client = MongoClient(connection_string)
    return  MongoClient(connection_string)['myzpt']['user']
