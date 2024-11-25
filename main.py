from face_recognition import capture_image, detect_face, save_face_to_db
from voice_recognition import capture_voice, encrypt_voice

def main():
    face_found = False
    
    # Keep retrying facial recognition until a face is found
    while not face_found:
        confirmation = input("Do you want to proceed with facial recognition? (yes/no): ").lower()
        if confirmation == 'yes':
            # Capture face image
            img_name = capture_image()
            face_img = detect_face(img_name)
            
            if face_img:
                save_face_to_db(face_img)  # Save the detected face image to MongoDB
                print("Facial recognition successful.")
                face_found = True
            else:
                print("No face detected. Retrying...")
        else:
            print("Facial recognition is required to proceed.")
    
    # Once the face is recognized, proceed to voice recognition
    voice_file = capture_voice()
    encrypt_voice(voice_file)  # Encrypt the voice file

if __name__ == "__main__":
    main()
