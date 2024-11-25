from bson.objectid import ObjectId
from database import check_image_saved

def save_image_to_file(image_data, filename):
    """Save the retrieved image data to a file."""
    with open(filename, 'wb') as f:
        f.write(image_data)
    print(f"Image saved as {filename}")

if __name__ == "__main__":
    # Example usage (replace with the actual ObjectId of the image you saved)
    image_id = ObjectId('your_image_id_here')  # Replace with your actual ObjectId
    image_data = check_image_saved(image_id)

    if image_data:
        save_image_to_file(image_data, 'retrieved_image.jpg')
