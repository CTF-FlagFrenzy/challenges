import hashlib
import os

import pycw

challengekey = "01JHQ6WHZMBCSEGDTF9Y8YFC99"
teamkey = os.getenv("TEAMKEY")

flaghash = hashlib.sha256(("%s%s" % (challengekey, teamkey)).encode()).hexdigest()
flag = "FF{%s}" % flaghash

pycw.output_wave("tones.wav", flaghash, 24, 20000)
# pycw.output_wave('base.wav', 'Some truths whisper, barely a breath above silence. Only those who listen beyond the range of hearing will find the key.', 24, 500)
