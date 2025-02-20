import hashlib, os, zlib, base64, pickle

teamkey = os.getenv("TEAMKEY")
challenge = os.getenv("CHALLENGEKEY")

flag = "%s%s" % (teamkey, challenge)
flaghash = (hashlib.sha256(flag.encode()).hexdigest())
hashed_flag = "FF{%s}" % flaghash

enc = base64.urlsafe_b64encode(zlib.compress(bytes(hashed_flag, 'utf-8')))
with open('flag', 'wb') as f:
    pickle.dump(enc, f)
    