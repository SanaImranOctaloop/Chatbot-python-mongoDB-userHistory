from mongodb.connection import get_database

db = get_database()

collection = db['conversation']
new_user = {"name": "Ali", "age": 22, "role": "Web Developer"}

insert_user = collection.insert_one(new_user)
print(f"Inserted document ID: {insert_user.inserted_id}")

find_user = collection.find_one({"name": "Ali"})
print("Retrieved User:", find_user)

update_user = collection.update_one({"name": "Ali"}, {"$set": {"role": "AI Engineer"}})
print("Updated Ali's role.")

read_updated_user = collection.find_one({"name": "Ali"})
print("Updated User:", read_updated_user)