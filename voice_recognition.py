import sounddevice as sd
import numpy as np
import wavio
from Crypto.Cipher import AES
import os
import tkinter as tk
from tkinter import messagebox

def capture_voice(filename='captured_voice.wav', duration=5):
    """
    Capture audio from the microphone, with an option to save or cancel.
    A Tkinter window shows a preview that voice is being recorded.
    """
    # Create a Tkinter window for the preview
    root = tk.Tk()
    root.title("Voice Recording Preview")
    
    # Set window size
    root.geometry("300x150")
    
    # Create a label to show the recording status
    label = tk.Label(root, text="Recording in progress...", font=("Arial", 16))
    label.pack(pady=50)
    
    # Start the Tkinter window in a separate thread so it doesn't block the audio recording
    root.after(5000, root.quit)  # Close window after the recording time
    
    # Show the window
    root.update()

    try:
        # Record audio
        print("Recording... Speak now.")
        audio = sd.rec(int(duration * 44100), samplerate=44100, channels=2, dtype='int16')
        sd.wait()  # Wait until recording is finished
        
        # Check if audio is captured
        if np.any(audio):
            print("Audio recorded successfully.")
        else:
            print("No audio detected. Check your microphone.")
            root.destroy()
            return None
        
        # Playback the recorded audio for user confirmation
        print("Playback: Listening to your recording...")
        sd.play(audio, samplerate=44100)
        sd.wait()  # Wait until playback is finished

        # Prompt user to save or discard the recording
        while True:
            user_input = input("Do you want to save this recording? (yes/no): ").strip().lower()
            if user_input in ['yes', 'y']:
                wavio.write(filename, audio, 44100, sampwidth=2)
                print(f"Voice saved as {filename}")
                root.destroy()
                return filename
            elif user_input in ['no', 'n']:
                print("Recording discarded.")
                root.destroy()
                return None
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
    except Exception as e:
        print(f"Error capturing audio: {e}")
        root.destroy()
        return None

def encrypt_voice(voice_file, output_file='encrypted_voice.enc'):
    """
    Encrypt the captured voice file using AES encryption.
    """
    if not voice_file:
        print("No voice file to encrypt.")
        return

    try:
        key = os.urandom(16)  # AES requires a key of 16, 24, or 32 bytes
        cipher = AES.new(key, AES.MODE_EAX)

        with open(voice_file, 'rb') as file:
            plaintext = file.read()

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        # Save the encrypted file
        with open(output_file, 'wb') as enc_file:
            enc_file.write(cipher.nonce + tag + ciphertext)

        print(f"Voice file encrypted and saved as {output_file}.")
        print(f"Encryption key (save securely): {base64.b64encode(key).decode()}")
    except Exception as e:
        print(f"Error encrypting voice file: {e}")

# Main Program Workflow
if __name__ == "__main__":
    print("Voice Recording and Encryption System")
    print("------------------------------------")

    # Step 1: Capture voice
    voice_file = capture_voice()

    # Step 2: Encrypt voice file if saved
    if voice_file:
        encrypt_voice(voice_file)
    else:
        print("No voice file to process further.")
