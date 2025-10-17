# debug_mongo_client.py
from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME

client = MongoDBClient(database_name=DATABASE_NAME)
print("Has attribute 'database'? ->", hasattr(client, "database"))
try:
    db = client.database
    print("database repr:", db)
    print("Collections:", db.list_collection_names()[:50])
    coll = db["Proj1-data"]
    print("Proj1-data count:", coll.count_documents({}))
except Exception as e:
    print("ERROR:", e)
