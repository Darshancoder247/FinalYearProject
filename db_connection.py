from pymongo import MongoClient

def get_db_connection():
    """Create and return a MongoDB database connection."""
    client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
    db = client['your_database_name']  # Replace with your database name
    return db
