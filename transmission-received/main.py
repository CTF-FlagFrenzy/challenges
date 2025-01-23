import PIL.Image
import qrcode
import os
import hashlib
import zbase32

challengekey = os.getenv('CHALLANGEKEY')
teamkey = os.getenv('TEAMKEY')

flaghash = zbase32.encode(hashlib.sha256(('%s%s' % (teamkey, challengekey)).encode()).digest())
print (flaghash)
flag = 'FF{%s}' % flaghash

code = qrcode.QRCode(box_size=4, border=1)
code.add_data(flag)
code.make(fit=False)
im = code.make_image()
#im.show()

fgimage = im.get_image()
bgimage = PIL.Image.open('bg.png')

bgimage.paste(fgimage, (90,96))
bgimage.save('placed.png')