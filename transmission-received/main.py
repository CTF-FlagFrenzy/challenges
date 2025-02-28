import PIL.Image
import qrcode
import os
import hashlib

challengekey = os.getenv('CHALLANGEKEY')
teamkey = os.getenv('TEAMKEY')

flaghash = hashlib.sha256(('%s%s' % (challengekey, teamkey)).encode()).hexdigest()
print (flaghash)
flag = 'FF{%s}' % flaghash

code = qrcode.QRCode(box_size=4, border=1)
code.add_data(flag)
code.make(fit=False)
im = code.make_image()
#im.show()

fgimage = im.get_image()
bgimage = PIL.Image.open('bg.png')

bgimage.paste(fgimage, (82, 67))
bgimage.save('placed.png')