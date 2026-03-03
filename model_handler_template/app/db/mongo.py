import urllib
import pymongo
import os

MODEL_COLLECTION = "models"

DB_NAME = "handler_db"

mongo_user = urllib.parse.quote_plus(os.environ.get("MONGOUSER", "user"))
mongo_password = urllib.parse.quote_plus(os.environ.get("MONGOPASSWORD", "password"))
mongo_URL = os.environ.get("MONGOHOST", "localhost")
print("mongodb://%s:%s@%s/" % (mongo_user, mongo_password, mongo_URL))
# Set up required endpoints.
mongo_client = pymongo.MongoClient(
    "mongodb://%s:%s@%s/" % (mongo_user, mongo_password, mongo_URL)
)


def get_model_collection():
    db = mongo_client[DB_NAME]
    return db[MODEL_COLLECTION]