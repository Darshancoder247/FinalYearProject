import os
from Crypto.Cipher import AES

# Create 'data/' folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

def encrypt_voice(voice_file):
    """Encrypt the captured voice file."""
    key = os.urandom(16)
    cipher = AES.new(key, AES.MODE_EAX)
    
    with open(voice_file, 'rb') as file:
        plaintext = file.read()
    
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    # Save encrypted data in 'data/' folder
    encrypted_voice_file = os.path.join('data', 'encrypted_voice.enc')
    with open(encrypted_voice_file, 'wb') as f:
        f.write(ciphertext)
    
    print(f"Voice file encrypted and saved as {encrypted_voice_file}")
    return encrypted_voice_file
