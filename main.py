from fastapi import FastAPI
from schema import User, Conversation
import db

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Welcome to the app!'}

@app.get('/all')
def get_all():
    data = db.all()
    return {'Data' : data}

@app.post('/createUser')
def create(user: User):
    user = db.createUser(user.username, user.password, user.email)
    return {'Instance inserted':True, 'User ID':user}

@app.post('/createConv')
def create(conv: Conversation):
    conversation = db.createConv(conv.userID, conv.conversations, conv.query, conv.botResponse)
    return {'Instance inserted':True, 'Conversation ID':conversation}