import base64
import random
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

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

random.shuffle(words)

def encrypt_flag(flag, key):
    iv = os.urandom(16)
    key = os.urandom(16)
    cipher = Cipher(algorithms.AES(key.encode()), modes.CBC(iv), backend=default_backend())
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_flag = padder.update(flag.encode()) + padder.finalize()
    encryptor = cipher.encryptor()
    encrypted_flag = encryptor.update(padded_flag) + encryptor.finalize()
    encrypted_flag_with_iv = base64.b64encode(iv + encrypted_flag).decode()
    return encrypted_flag_with_iv

strencfunc = f"""
def {words[0]}({words[1]}, {words[2]}):
    {words[3]} = {os.urandom(16)}
    {words[2]} = {os.urandom(16)}
    {words[4]} = Cipher(algorithms.AES({words[2]}.encode()), modes.CBC({words[3]}), backend=default_backend())
    {words[5]} = padding.PKCS7(algorithms.AES.block_size).padder()
    {words[6]} = {words[5]}.update({words[1]}.encode()) + {words[5]}.finalize()
    {words[7]} = {words[4]}.encryptor()
    {words[8]} = {words[7]}.update({words[6]}) + {words[7]}.finalize()
    {words[9]} = base64.b64encode({words[3]} + {words[8]}).decode()
    return {words[9]}
"""
print(strencfunc)


with open ("obfuscated.py", "wb") as f:
    import_statements = """
    import base64 \n
    import random \n
    import os \n
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes \n
    from cryptography.hazmat.primitives import padding \n
    from cryptography.hazmat.backends import default_backend \n
    """
    f.write(import_statements.encode())
