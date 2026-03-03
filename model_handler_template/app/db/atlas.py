import os

from pymongo import MongoClient

DB_NAME = "task_rating"
COLLECTION_NAME = "informal"

atlas_client : MongoClient = MongoClient(os.environ["ATLAS_URI"])
rating_db = atlas_client[DB_NAME]
rating_collection = rating_db[COLLECTION_NAME]

info = atlas_client.server_info()  # This should error, if the client doesn't work
print(info)
class AtlasClient ():

   def __init__ (self, altas_uri, dbname):
       self.mongodb_client = MongoClient(altas_uri)
       self.database = self.mongodb_client[dbname]

   def ping (self):
       self.mongodb_client.admin.command('ping')

   def get_collection (self, collection_name):
       collection = self.database[collection_name]
       return collection

   def find (self, collection_name, filter = {}, limit=0):
       collection = self.database[collection_name]
       items = list(collection.find(filter=filter, limit=limit))
       return items


def get_atlas_collection():
    return rating_collection
    