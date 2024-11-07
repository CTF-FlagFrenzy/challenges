import base64
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

team_key = "Team1"
challenge_key = "reversing-I"
combined_flag = challenge_key + team_key
hashed_flag = f"FF{{{hashlib.md5(combined_flag.encode()).hexdigest()}}}"

print(f"Flag: {hashed_flag}")


def encrypt_flag(flag, key):
    # Create a 16-byte IV (Initialization Vector)
    iv = os.urandom(16)
    
    # Create a cipher object using the key and IV
    cipher = Cipher(algorithms.AES(key.encode()), modes.CBC(iv), backend=default_backend())
    
    # Pad the flag to be a multiple of the block size (16 bytes for AES)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_flag = padder.update(flag.encode()) + padder.finalize()
    
    # Encrypt the padded flag
    encryptor = cipher.encryptor()
    encrypted_flag = encryptor.update(padded_flag) + encryptor.finalize()
    
    # Combine the IV and the encrypted flag and encode it in base64
    encrypted_flag_with_iv = base64.b64encode(iv + encrypted_flag).decode()
    
    return encrypted_flag_with_iv

decrypt_func ="""
def decrypt_flag(funny, HEHEHA):
    funny = base64.b64decode(funny)
    what = funny[:16]
    is_this_aFlag = funny[16:]
    kkkkkkkkkk = Cipher(algorithms.AES(HEHEHA.encode()), modes.CBC(what), backend=default_backend())
    decryptor = kkkkkkkkkk.decryptor()
    OOOOOOOOoOoO = decryptor.update(is_this_aFlag) + decryptor.finalize()
    whoamI = padding.PKCS7(algorithms.AES.block_size).padder()
    ballin = whoamI.update(OOOOOOOOoOoO) + whoamI.finalize()
    return ballin.decode()
"""


with open("decryptfunc.txt", "wb") as f:
    f.write(base64.b64encode(decrypt_func.encode()))


exec(decrypt_func)



# Example usage
key = "ballsballsballs3"  # Key must be 16, 24, or 32 bytes long
encrypted_flag = encrypt_flag(hashed_flag, key)
exec(decrypt_func)
print(f"Encrypted Flag: {encrypted_flag}")
print(f"Decrypted Flag: {decrypt_flag(encrypted_flag, key)}")
