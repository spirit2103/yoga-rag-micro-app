from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["yogaRAG"]

chunks_collection = db["chunks"]      # vector + content
queries_collection = db["queries"]    # logs
feedback_collection = db["feedback"]
