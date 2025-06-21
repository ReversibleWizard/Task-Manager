from pymongo import MongoClient
import os

client = None
db = None
tasks_collection = None
users_collection = None

def init_db(app):
    global client, db, tasks_collection, users_collection
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_uri)
    db = client['task_manager']
    tasks_collection = db['tasks']
    users_collection = db['users']
