from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Global variable for MongoDB client
mongo_client = None

def get_database():
    global mongo_client

    if mongo_client is None:
        MONGODB_URI = os.getenv("MONGODB_URI")

        if not MONGODB_URI:
            logging.error("MONGODB_URI is not set in the .env file")
            raise Exception("MONGODB_URI is missing in .env file")

        try:
            # Initialize MongoDB Client with Connection Pooling
            mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)

            # Test the connection
            mongo_client.admin.command('ping')

            logging.info("Connected to MongoDB successfully!")

        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise Exception(f"MongoDB Connection Error: {e}")

    return mongo_client["chatbot"]
