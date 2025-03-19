import base64
import hashlib
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Retrieve the parts from their respective locations
part_a = "..."  # Retrieve from /etc/passwd
part_b = "..."  # Retrieve from /home/j007/confs/backup_42.conf
part_c = "..."  # Retrieve from /home/j007/notes.txt
part_d = "..."  # Retrieve from /var/log/syslog
hex_iv = "..."  # Retrieve from /home/j007/notes.txt

# Combine all parts to form the original ciphertext
hex_ciphertext = part_a + part_b + part_c + part_d

# Convert the hexadecimal ciphertext and IV to bytes
ciphertext = bytes.fromhex(hex_ciphertext)
iv = bytes.fromhex(hex_iv)

# Use the AES key and IV to decrypt the ciphertext
hashed_flag = "FF{...}"  # The hashed flag used to generate the AES key
aes_key = hashed_flag[:16].encode('utf-8')  # 16-byte key

cipher = AES.new(aes_key, AES.MODE_CBC, iv)
decrypted_padded = cipher.decrypt(ciphertext)
decrypted_flag = unpad(decrypted_padded, AES.block_size).decode('utf-8')

print(f"Decrypted Flag: {decrypted_flag}")