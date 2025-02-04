from connection import get_database
from schema import UserSignup, Message, UpdatePassword
from bson import ObjectId
from auth import hash_password, verify_password


# Creating Database
db = get_database()
users_collection = db["users"]
conv_collection = db["conversations"]



# CREATE 
def createUser(user: UserSignup):
    if users_collection.find_one({"$or": [{"Username": user.username}, {"Email": user.email}]}):
        return {"error": "Username or Email already exists."}
    user_data = {
        "Username": user.username,
        "Email": user.email,
        "Hashed_Password": hash_password(user.password), 
        "Conversations": []
    }
    response = users_collection.insert_one(user_data)
    return str(response.inserted_id)


def createConv(username: str, query: str, response: str) -> dict:
    message = dict(Message(query=query, response=response))
    conversation_data = {
        "Username": username,
        "Chat": [message]
    }
    try:
        result = conv_collection.insert_one(conversation_data)
        convID = str(result.inserted_id)
        users_collection.update_one(
            {"Username": username},
            {"$push": {"Conversations": convID}}
        )
        return {"success": True, "conversation_id": convID, "chat": conversation_data}
    except Exception as e:
        return {"error": f"Failed to create conversation: {str(e)}"}




# READ 
def allUsers():
    return [{**user, "_id": str(user["_id"]), "Hashed_Password": "HIDDEN"} 
            for user in users_collection.find({}, {"Hashed_Password": 0})]


def get_oneUser(username):
    user = users_collection.find_one({"Username": username}, {"Hashed_Password": 0})
    if not user:
        return {"error": "User not found."}
    user["_id"] = str(user["_id"])
    return user


def allConv():
    return [{**conv, "_id": str(conv["_id"])} for conv in conv_collection.find({})]


def get_oneConv(convID):
    try:
        conv = conv_collection.find_one({"_id": ObjectId(convID)})
        if not conv:
            return {"error": "Conversation not found."}
        conv["_id"] = str(conv["_id"])
        return conv
    except:
        return {"error": "Invalid conversation ID format"}



# UPDATE 
def updateUsername(username, new_username):
    result = users_collection.update_one({"Username": username}, {"$set": {"Username": new_username}})
    return result.modified_count > 0


def updateUserPassword(username, update_data: UpdatePassword):
    user = users_collection.find_one({"Username": username})
    if not user:
        return {"error": "User not found."}
    if not verify_password(update_data.old_password, user["Hashed_Password"]):
        return {"error": "Incorrect old password."}
    hashed_new_password = hash_password(update_data.new_password)
    result = users_collection.update_one(
        {"Username": username},
        {"$set": {"Hashed_Password": hashed_new_password}}
    )
    return result.modified_count > 0


def updateConv(convID: str, query: str, response: str) -> dict:
    try:
        if not conv_collection.find_one({"_id": ObjectId(convID)}):
            return {"error": "Conversation not found."}

        new_message = dict(Message(query=query, response=response))
        conv_collection.update_one(
            {"_id": ObjectId(convID)},
            {"$push": {"Chat": new_message}}
        )
        return {"success": True, "message": "Conversation updated."}
    except:
        return {"error": "Invalid conversation ID format"}




# DELETE 
def deleteUser(username):
    user = users_collection.find_one({"Username": username})
    if not user:
        return {"error": "User not found."}
    conv_collection.delete_many({"UserID": str(user["_id"])})
    result = users_collection.delete_one({"Username": username})
    return result.deleted_count > 0


def deleteConv(convID):
    try:
        result = conv_collection.delete_one({"_id": ObjectId(convID)})
        return result.deleted_count > 0
    except:
        return {"error": "Invalid conversation ID format"}
