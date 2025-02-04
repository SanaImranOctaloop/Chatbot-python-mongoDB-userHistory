from fastapi import FastAPI, Depends, HTTPException
from schema import UserSignup, Login, UpdatePassword
from db import users_collection
from LLM import new_chat_with_mistral, existing_chat_with_mistral
from auth import get_current_user, verify_password, create_access_token, oauth2_scheme
import db, uvicorn

app = FastAPI()



# ROOT ROUTE 
@app.get("/")
def root():
    return {"message": "Welcome to the app!"}



# AUTHENTICATION ROUTES 
@app.post("/signup")
def signup(user: UserSignup):
    userID = db.createUser(user)
    if "error" in userID:
        raise HTTPException(status_code=400, detail=userID["error"])
    return {"success": True, "message": "User created successfully", "user_id": userID}


@app.post("/login")
def login(user: Login):
    user_data = users_collection.find_one({"Username": user.username})
    if not user_data or not verify_password(user.password, user_data["Hashed_Password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"success": True, "access_token": token, "token_type": "bearer"}



# CHATBOT ROUTE 
@app.post("/add_chat/{convID}")
def chat_with_ai(convID: str, user_query: str, token: str = Depends(oauth2_scheme)):
    response = existing_chat_with_mistral(convID, user_query)
    return {"success": True, "response": response}


@app.post("/new_chat/{username}")
def new_chat_with_ai(username: str, user_query: str, token: str = Depends(oauth2_scheme)):
    response = new_chat_with_mistral(username, user_query)
    return {"success": True, "response": response}



# USER ROUTES 
@app.get("/allUsers")
def get_all_users(token: str = Depends(oauth2_scheme)):
    data = db.allUsers()
    return {"success": True, "data": data}


@app.get("/getUser/{username}")
def get_user(username: str, current_user: str = Depends(get_current_user)):
    if username != current_user:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    data = db.get_oneUser(username)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return {"success": True, "data": data}



@app.put("/updatePassword/{username}")
def update_password(username: str, update_data: UpdatePassword, token: str = Depends(oauth2_scheme)):
    result = db.updateUserPassword(username, update_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"success": True, "message": "Password updated successfully"}


@app.delete("/deleteUser/{username}")
def delete_user(username: str, token: str = Depends(oauth2_scheme)):
    if db.deleteUser(username):
        return {"success": True, "message": "User deleted"}
    raise HTTPException(status_code=400, detail="Failed to delete user")



# CONVERSATION ROUTES 
# @app.post("/createConv")
# def create_conversation(userID: str, query: str, response: str, token: str = Depends(oauth2_scheme)):
#     conv_id = db.createConv(userID, query, response)
#     if "error" in conv_id:
#         raise HTTPException(status_code=400, detail=conv_id["error"])
#     return {"success": True, "message": "Conversation created", "conversation_id": conv_id}


@app.get("/allConv")
def get_all_conversations(token: str = Depends(oauth2_scheme)):
    data = db.allConv()
    return {"success": True, "data": data}


@app.get("/getConv/{convID}")
def get_conversation(convID: str, token: str = Depends(oauth2_scheme)):
    data = db.get_oneConv(convID)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return {"success": True, "data": data}


@app.put("/updateConversation/{convID}")
def update_conversation(convID: str, query: str, response: str, token: str = Depends(oauth2_scheme)):
    update_status = db.updateConv(convID, query, response)
    if "error" in update_status:
        raise HTTPException(status_code=404, detail=update_status["error"])
    return {"success": True, "message": "Conversation updated"}


@app.delete("/deleteConv/{convID}")
def delete_conversation(convID: str, token: str = Depends(oauth2_scheme)):
    if db.deleteConv(convID):
        return {"success": True, "message": "Conversation deleted"}
    raise HTTPException(status_code=400, detail="Failed to delete conversation")



# RUN SERVER 
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
