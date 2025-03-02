import hashlib, os, zlib, base64, pickle

teamkey = os.getenv("TEAMKEY")
challengekey = '01JEB55RPNPJW08X1GB5SR03DF'

flag = "%s%s" % (challengekey, teamkey)
flaghash = (hashlib.sha256(flag.encode()).hexdigest())
hashed_flag = "FF{%s}" % flaghash

enc = base64.urlsafe_b64encode(zlib.compress(bytes(hashed_flag, 'utf-8')))
with open('flag', 'wb') as f:
    pickle.dump(enc, f)
    