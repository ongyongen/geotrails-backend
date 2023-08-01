from pymongo.mongo_client import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')

# Create a new client and connect to the server
try:
    client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())

    db = client.geocaches
    geocaches_collection = db["caches"]
    users_collection = db["users"]
    users_analytics_collection = db["records"]

    client.admin.command('ping')
    print("You successfully connected to MongoDB!")
except Exception as e:
    print(e)