from fastapi import FastAPI
from schema import User, Conversation
import uvicorn
import db

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Welcome to the app!'}



# Create
@app.post('/createUser')
def create(user: User):
    User = db.createUser(user.username, user.password, user.email)
    return {'Instance inserted':True, 'User ID':User}

@app.post('/createConv')
def create(conv: Conversation):
    conversation = db.createConv(conv.userID, conv.conversations, conv.query, conv.response, conv.chat)
    return {'Instance inserted':True, 'Conversation ID':conversation}



# Read
@app.get('/allUsers')
def get_allUsers():
    data = db.allUsers()
    return {'Data' : data}

@app.get('/get/{username}')
def get_oneUser(username:str):
    data = db.get_oneUser(username)
    return {"data" : data}

@app.get('/allConv')
def get_allConv():
    data = db.allConv()
    return {'Data' : data}

@app.get('/get/{convID}')
def get_oneConv(convID:str):
    data = db.get_oneConv(convID)
    return {"data" : data}



# Update
@app.put('/updateUsername')
def updateUsername(data:schema.User):
    data = db.updateUsername(data)
    return {'updated' : True, 'Updated Instance' : data}

@app.put('/update/{password}')
def updatePassword(password, data):
    change = db.updatePassword(password, data)
    return {'updated' : True, 'Updated Instance' : change}



# Delete
@app.delete('/deleteUser')
def deleteUser(username:str):
    data = db.deleteUser(username)
    return {'deleted': True, 'Deleted Instance': data}

@app.delete('/deleteConv')
def deleteConv(ConvID:str):
    data = db.deleteConv(ConvID)
    return {'deleted': True, 'Deleted Instance': data}



# Run App
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)