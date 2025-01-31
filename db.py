from connection import get_database

db = get_database()
users_collection = db['users']
conv_collection = db['conversations']

# new_user = {"Username": "aleena123", "Password": "ww22", "Email": "aleena123@gmail.com"}

# insert_user = users_collection.insert_one(new_user)
# print(f"Inserted document ID: {insert_user.inserted_id}")



def createUser(username:str, password:str, email:str):
    conversations = []
    history = {}
    data = {"Username": username, "Password": password, "Email": email,
            "Conversations List": conversations, "History": history}
    response = users_collection.insert_one(data)
    return str(response.inserted_id)

def createConv(userID:str, conversations:list, query:str, response:str, chat:list):
    chat = [{"Query": query, "Response": response}]
    data = {"UserID": userID, "Chat": chat }
    Response = conv_collection.insert_one(data)
    convID = str(Response.inserted_id)
    conversations.append(convID)
    return convID

def allUsers():
    response = users_collection.find({})
    return list(response)

def get_one(userID):
    return users_collection.find_one({'userID' : userID})

def update(id, data):
    response = users_collection.update_one({'userID':id, '$set':data})
    return response.modified_count

def delete(userID):
    response = users_collection.delete_one({'userID':userID})
    return response.deleted_count