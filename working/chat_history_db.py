import os 
import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

client = MongoClient(MONGODB_URI)

db = client["Chatbot"]
users_collection = db["Users"]
convo_collection = db["Conversations"]

userID = 1
users = [1, 2, 3]

conversationID = 1
conversations_ids = [2, 3, 4]

history = { 
    0 : 
    [
        {
            "user" : "hello", 
            "bot": "Hi, how can I assist you?"
        },
        {
            "user" : "I'm a writer and I want your assistance in writing a paragraph.", 
            "bot": "Sure, I would like to assist you. Please tell some title or topic to write a paragraph about."
        }
    ],
    1 : 
    [
        {
            "user" : "hi, I'm Sana", 
            "bot": "Hi, Sana! how can I assist you?"
        },
        {
            "user" : "I'm a learner of backend programming help me.", 
            "bot": "Sure, I would like to assist you. Please tell some details about the topic you want to learn."
        }
    ],
    }

for convo in conversations_ids:
    history[convo] = [
        { 
            "user" : "this is user query.",
            "bot" : "this is the chatbot response."
        },
        { 
            "user" : "Another user query in same chat.",
            "bot" : "Another chatbot response."
        },
    ]

#print(history)

new_user = {
    'userID' : userID,
    'history' : history
}

new_convo = {
    "conversationID" : 1,
    "chat" : [
        {
            'user': '',
            'bot' : ''
        },
        {
            'user': '',
            'bot' : ''
        }
    ]
}