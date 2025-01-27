# Importing Libraries
import os 
from dotenv import load_dotenv
from pymongo import MongoClient

# Loading Environment Variables
load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

# Creating a MongoDB Client
client = MongoClient(MONGODB_URI)

# Enlisting all the databases in a cluster
for db_name in client.list_database_names():
    print(db_name)
    
client.close() 