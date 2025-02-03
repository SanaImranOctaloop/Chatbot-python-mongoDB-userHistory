from connection import get_database
from schema import User, Conversation
from bson import ObjectId


# Create Database and Tables
db = get_database()
users_collection = db['users']
conv_collection = db['conversations']

# new_user = {"Username": "aleena123", "Password": "ww22", "Email": "aleena123@gmail.com"}

# insert_user = users_collection.insert_one(new_user)
# print(f"Inserted document ID: {insert_user.inserted_id}")



# Create
def createUser(username:str, password:str, email:str):
    if users_collection.find_one({"Username": username}, {"Email": email}):
        return {"error" : "User already exists."}
    
    user_data = {
        "Username": username,
        "Password": password,
        "Email": email,
        "Conversations": [],
        }
    response = users_collection.insert_one(user_data)
    return str(response.inserted_id)
    

def createConv(userID:str, query:str, response:str):
    message = {"Query": query, "Response": response}
    conversation_data = {
        "UserID": userID, 
        "Chat": [message] 
        }
    Response = conv_collection.insert_one(conversation_data)
    convID = str(Response.inserted_id)

    users_collection.update_one(
        {"_id": ObjectId(userID)},
        {"$push": {"Conversations": convID}}
    )
    return convID



# Read
def allUsers():
    response = users_collection.find({})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data

def get_oneUser(username):
    response = users_collection.find_one({'Username' : username})
    response["_id"] = str(response["_id"])
    return response

def allConv():
    response = conv_collection.find({})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data

def get_oneConv(convID):
    response = conv_collection.find_one({'_id' : convID})
    response["_id"] = str(response["_id"])
    return response



# Update
def updateUsername(data):
    data = dict(data)
    response = users_collection.update_one({'Username':data["Username"]}, {'$set':{"Username": data["Username"]}})
    response['_id'] = str(response['_id'])
    return response.modified_count

def updateUserPassword(data):
    data = dict(data)
    response = users_collection.update_one({'Password':data["Password"]}, {'$set':{"Password": data["Password"]}})
    response['_id'] = str(response['_id'])
    return response.modified_count



# Delete
def deleteUser(username):
    response = users_collection.delete_one({'Username':username})
    response['_id'] = str(response['_id'])
    return response.deleted_count

def deleteConv(convID):
    response = conv_collection.delete_one({'_id':convID})
    response['_id'] = str(response['_id'])
    return response.deleted_count