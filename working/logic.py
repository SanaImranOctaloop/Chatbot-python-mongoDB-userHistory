# Importing Libraries
import os 
import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

# Loading Environment Variables
load_dotenv()
#MONGODB_URI = os.environ["MONGODB_URI"]

# Creating a MongoDB Client
#client = MongoClient(MONGODB_URI)

# Get reference to 'Chatbot' database
#db = client.chatbot

# Get reference to 'Users' table
#users_collection = db.users

users = []
# User class
class User:
    def __init__(self, userID: int):
        self.userID = userID
        conversationIDs = []
        history = {}
    
    def start_conversation(self):
        if self.userID not in users:
            users.append(self.userID)

# Create a new user
new_user = {
    'userID' : 1,
    'conversationID' : 1,
    'conversations' : [],
    'history' : {}
}

# Enlisting all the databases in a cluster
#for db_name in client.list_database_names():
#    print(db_name)
    
#client.close() 