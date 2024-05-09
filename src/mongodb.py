from pymongo import MongoClient
from datetime import datetime
import json
import os

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['snake_game_db']
collection = db['game_sessions']

# File and database operations
def check_database_file_exists(file_path):
    return os.path.exists(file_path) and os.path.getsize(file_path) > 0

def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def store_game_result(player_name, score):
    document = {
        'player_name': player_name,
        'score': score,
        'date': datetime.now()
    }
    collection.insert_one(document)
    print(f"Game result saved for {player_name} with score {score}")

def fetch_all_game_results():
    return list(collection.find({}))

def initialize_database_from_file(file_path):
    if check_database_file_exists(file_path):
        data = read_data_from_file(file_path)
        if data:  # Ensure data is not empty
            collection.insert_many(data)

def convert_to_json_serializable(documents):
    for doc in documents:
        if 'date' in doc and isinstance(doc['date'], datetime):
            doc['date'] = doc['date'].isoformat()  # Convert datetime to ISO format string
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
    return documents
def dump_data_to_json(file_path):
    data = fetch_all_game_results()
    data = convert_to_json_serializable(data)
    write_data_to_file(data, file_path)
def clear_database():
    collection.delete_many({})

def clear_output_json(file_path):
    with open(file_path, 'w') as file:
        file.write('[]')

def check_data():
    documents = collection.find()
    # Print each document
    for document in documents:
        print(document)