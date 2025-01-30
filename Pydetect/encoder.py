import zlib, pickle
from base64 import urlsafe_b64encode as b64enc

flag = open('flag.txt', 'r').read()
enc = b64enc(zlib.compress(bytes(flag, 'utf-8')))
with open('flag', 'wb') as f:
    pickle.dump(enc, f)

