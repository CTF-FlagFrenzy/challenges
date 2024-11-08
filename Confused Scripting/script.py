import base64, random, hashlib, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

team_key = "Team1"
challenge_key = "reversing-I"
combined_flag = challenge_key + team_key
hashed_flag = f"FF{{{hashlib.md5(combined_flag.encode()).hexdigest()}}}"

print(f"Flag: {hashed_flag}")


#a list of names, that will be hashed and used as names for functions and variables
words = [
    "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew",
    "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry",
    "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yellowfruit",
    "zucchini", "apricot", "blackberry", "blueberry", "cantaloupe", "clementine",
    "dragonfruit", "grapefruit", "guava", "jackfruit", "kumquat", "lime", "lychee",
    "mandarin", "mulberry", "olive", "passionfruit", "peach", "pear", "persimmon",
    "pineapple", "plum", "pomegranate", "starfruit", "tamarind", "tomato", "avocado",
    "bilberry", "boysenberry", "currant", "damson", "feijoa", "gooseberry", "jabuticaba",
    "jambul", "jujube", "longan", "loquat", "medlar", "miraclefruit", "mulberry",
    "nance", "pawpaw", "pitanga", "pitaya", "plantain", "rambutan", "redcurrant",
    "salak", "soursop", "surinamcherry", "tamarillo", "whitecurrant", "yuzu",
    "ackee", "akee", "ambarella", "babaco", "bignay", "breadfruit", "burdekinplum",
    "calamondin", "canistel", "capulincherry", "carambola", "cherimoya", "chico",
    "cupuacu", "durian", "genip", "grumichama", "ilama", "imbe", "jocote", "kaki",
    "kepel", "langsat", "lucuma", "mamey", "mamoncillo", "marang", "marula", "matoa",
    "mombin", "monstera", "muscadine", "naranjilla", "noni", "pandanus", "pequi",
    "pulasan", "santol", "sapodilla", "sapotilla", "soursop", "tamarind", "tangelo",
    "tangor", "ugli", "voavanga", "wampi", "whitecurrant", "yangmei", "yumberry",
    "ziziphus"
]

EncryptionKey = os.urandom(16)

#hash a string, until the first character is a string
#this is because using a int as a first letter of a function makes python cry
def create_md5_hash(text):
    hashed =  hashlib.md5(text.encode()).hexdigest()
    while hashed[0].isdigit():
        hashed = hashlib.md5(hashed.encode()).hexdigest()
    return hashed

# create a list of hashed words
words = [create_md5_hash(word) for word in words]

# shuffle the words to ensure that every file is unique
random.shuffle(words)

#the function that is encrypting the flag
def encrypt_flag(flag, key):
    iv = os.urandom(16)
    key = key
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_flag = padder.update(flag.encode()) + padder.finalize()
    encryptor = cipher.encryptor()
    encrypted_flag = encryptor.update(padded_flag) + encryptor.finalize()
    encrypted_flag_with_iv = base64.b64encode(iv + encrypted_flag).decode()
    return encrypted_flag_with_iv

#the function that is decrypting the flag, used for debug or solution
def decrypt(encrypted_text, key):
    encrypted_data = base64.b64decode(encrypted_text)
    iv = encrypted_data[:16]
    encrypted_flag = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_flag = decryptor.update(encrypted_flag) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    flag = unpadder.update(padded_flag) + unpadder.finalize()
    return flag.decode()

# the encryption function, but converted to be filled with random names for maximum confusion
strencfunc = f"""
def {words[0]}({words[1]}, {words[2]}):
    {words[3]} = {os.urandom(16)}
    {words[2]} = {EncryptionKey}
    {words[4]} = Cipher(algorithms.AES({words[2]}.encode()), modes.CBC({words[3]}), backend=default_backend())
    {words[5]} = padding.PKCS7(algorithms.AES.block_size).padder()
    {words[6]} = {words[5]}.update({words[1]}.encode()) + {words[5]}.finalize()
    {words[7]} = {words[4]}.encryptor()
    {words[8]} = {words[7]}.update({words[6]}) + {words[7]}.finalize()
    {words[9]} = base64.b64encode({words[3]} + {words[8]}).decode()
    return {words[9]}
"""

#the flag but encrypted using the encryption function
secured_flag = encrypt_flag(hashed_flag, EncryptionKey)

#write all of the script to a file dynamically
with open ("/usr/local/apache2/htdocs/obfuscated.py", "wb") as f:
    import_statements = """import base64
import random
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
"""
    hint = f"""\n\n\n\n#The output has been intercepted: {secured_flag}"""

    f.write(import_statements.encode())
    f.write(strencfunc.encode())
    f.write(hint.encode())


html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Download File</title>
</head>
<body>
    <a href="obfuscated.py" download="obfuscated.py">Download obfuscated.py</a>
</body>
</html>
"""

# Write HTML content to a file
output_path = "/usr/local/apache2/htdocs/index.html"
with open(output_path, "w") as file:
    file.write(html_content)

print(f"HTML file written to {output_path}")