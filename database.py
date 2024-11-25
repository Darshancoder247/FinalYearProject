from bson.objectid import ObjectId
from db_connection import get_db_connection

def insert_image(image_data):
    """Insert an image into the MongoDB collection."""
    db = get_db_connection()
    collection = db['your_collection_name']  # Replace with your collection name

    # Insert the image data into the collection
    image_document = {"image_data": image_data}  # Adjust the key as per your schema
    result = collection.insert_one(image_document)
    print(f"Image inserted with id: {result.inserted_id}")
    return result.inserted_id  # Return the ObjectId of the inserted image

def check_image_saved(image_id):
    """Check if an image is saved in MongoDB and return its data."""
    db = get_db_connection()
    collection = db['your_collection_name']  # Replace with your collection name

    # Find the image document by ID
    image_document = collection.find_one({"_id": image_id})
    
    if image_document:
        print("Image found in the database.")
        return image_document['image_data']  # Adjust this based on your schema
    else:
        print("No image found with that ID.")
        return None
