import pycw
import os
import hashlib

challengekey = os.getenv('CHALLANGEKEY')
teamkey = os.getenv('TEAMKEY')

flaghash = hashlib.sha256(('%s%s' % (teamkey, challengekey)).encode()).hexdigest()
flag = 'FF{%s}' % flaghash

pycw.output_wave('tones.wav', flaghash, 24, 20000)
#pycw.output_wave('base.wav', 'Some truths whisper, barely a breath above silence. Only those who listen beyond the range of hearing will find the key.', 24, 500)
