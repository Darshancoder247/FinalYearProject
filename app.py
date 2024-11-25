import os
import cv2
import time
import numpy as np
import mediapipe as mp
from flask import Flask, render_template, request, redirect, url_for, flash
from face_recognition import capture_image, detect_face
from voice_recognition import capture_voice  # Import your existing functions
import sounddevice as sd
import wave
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection

# Create a dictionary to store user information
user_data = {}

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store_info', methods=['GET', 'POST'])
def store_info():
    if request.method == 'POST':
        name = request.form['name']
        additional_info = request.form.get('additional_info', '')  # Optional additional info
        img_name = f'data/{name}.jpg'  # Save the face image with the name

        # Step 1: Capture and save the face image
        captured_face = capture_image(img_name)
        if not captured_face:
            flash("Face capture failed. Please try again.", "danger")
            return redirect(url_for('store_info'))

        # Step 2: Store user information in the dictionary
        user_data[name] = {"info": additional_info}  # Add user info in dict

        # Step 3: Prompt and save voice recording
        voice_file = f'data/{name}_voice.wav'
        captured_voice = capture_voice(voice_file)
        if captured_voice:
            user_data[name]["voice"] = voice_file
        else:
            flash("Voice not captured. Proceeding without voice.", "warning")

        # Step 4: Detect and store the face
        detected_face_path = detect_face(img_name)
        if detected_face_path:
            flash(f"Information stored for {name}.", "success")
            return redirect(url_for('index'))
        else:
            flash("Face detection failed. Please try again.", "danger")

    return render_template('store_info.html')

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'POST':
        name = request.form['name']  # Getting the name from the form
        img_name = f'data/{name}.jpg'  # Path to stored face image

        if name not in user_data:  # Check if user data exists
            flash(f"No data found for {name}.", "warning")
            return redirect(url_for('index'))  # Redirect to home if no user data is found

        # Step 1: Capture a new image for recognition
        captured_face = capture_image('data/captured_face.jpg')
        if not captured_face:
            flash("Face capture failed. Please try again.", "danger")
            return redirect(url_for('index'))  # Redirect if capture failed

        # Step 2: Detect the captured face
        detected_face_path = detect_face('data/captured_face.jpg')
        if detected_face_path:
            # Compare the detected face with the stored image
            stored_image = cv2.imread(img_name)
            detected_image = cv2.imread(detected_face_path)

            if np.array_equal(stored_image, detected_image):  # Simple image comparison
                user_info = user_data[name]["info"]
                flash(f"Welcome, {name}!", "success")

                # Optional: Voice playback for verification
                if "voice" in user_data[name]:  # Check if voice data is available
                    voice_file = user_data[name]["voice"]
                    play_voice(voice_file)  # Play the voice for verification

                return render_template('display_info.html', name=name, info=user_info)
            else:
                flash("Face not recognized. Please try again.", "danger")
        else:
            flash("No face detected in the captured image. Please try again.", "danger")

        return redirect(url_for('index'))  # Redirect if face recognition fails

    # GET request: Display the recognize page
    return render_template('recognize.html')

def play_voice(voice_file):
    """Play the captured voice for verification."""
    try:
        # Read and play the .wav file using SoundDevice
        with open(voice_file, 'rb') as f:
            wav_data = f.read()
        
        # Use io.BytesIO to simulate a file object for sounddevice playback
        audio_stream = io.BytesIO(wav_data)
        wav = wave.open(audio_stream, 'rb')
        sample_rate = wav.getframerate()
        frames = wav.readframes(wav.getnframes())

        # Play the voice data using sounddevice
        sd.play(frames, samplerate=sample_rate)
        sd.wait()
    except Exception as e:
        flash(f"Voice playback failed: {str(e)}", "danger")

if __name__ == '__main__':
    app.run(debug=True)
