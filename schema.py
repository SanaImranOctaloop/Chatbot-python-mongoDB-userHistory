from pydantic import BaseModel, EmailStr
from typing import List


class Message(BaseModel):
    query: str
    response: str


class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str 
    conversations: List[str] = []


class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str  

class Login(BaseModel):
    username: str
    password: str


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str


class Conversation(BaseModel):
    userID: str
    chat: List[Message]
    