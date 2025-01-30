from pydantic import BaseModel

class User(BaseModel):
    username : str
    password : str
    email: str
    conversations : list
    history : dict
    
    
class Conversation(BaseModel):
    userID : str
    conversations : list
    chat : list 
        