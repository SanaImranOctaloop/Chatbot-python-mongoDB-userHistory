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
    query : str
    response : str
    chat : list
    
    # def chats(self, query, response):
    #     self.query = query
    #     self.response = response
    #     return [{"Query": self.query, "Response": self.response}]
    
    # chat = chats()