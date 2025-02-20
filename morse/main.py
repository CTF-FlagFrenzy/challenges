import pycw
import os
import hashlib

challengekey = os.getenv('CHALLANGEKEY')
teamkey = os.getenv('TEAMKEY')

flaghash = hashlib.sha256(('%s%s' % (teamkey, challengekey)).encode()).hexdigest()
print (flaghash)
flag = 'FF{%s}' % flaghash

pycw.output_wave('tones.wav', flaghash, 24, 20000)
#pycw.output_wave('base.wav', 'The signal you seek is beyond what ears perceive. Only the keenest analysis will reveal the truth.', 24, 500)



