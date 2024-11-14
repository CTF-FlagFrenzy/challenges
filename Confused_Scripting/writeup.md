# CTF Web-Challenge | Confused Scripting Writeup: Easy Level

## Challenge Overview

In this challange the user is provided a python script, where he has the output of the function and has to essentially reverse one of the inputs of the function. The function looks something like this.

```py
import base64
import random
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def dec511f084772baf1f916b90eec6b42a(aa9eddcb39de50597424b155a6f7e043, f4382049c37f07c9d8ae892efd792247):
    a84b32590693190747d6019b6b735ac1 = b'\x1eu>c_\xe5_\xe1\x06\xc2\x0f\x04\xc1S\x04\x01'
    f4382049c37f07c9d8ae892efd792247 = b'}n\xb2\xe5i\xd3\xb9\x9b\x00\xdcZ\xec\x16\xd6\x10t'
    f8c2fea25e65a76d7339129e17164c40 = Cipher(algorithms.AES(f4382049c37f07c9d8ae892efd792247.encode()), modes.CBC(a84b32590693190747d6019b6b735ac1), backend=default_backend())
    f28c2c1585824cc28d5bc045cf4c5b13 = padding.PKCS7(algorithms.AES.block_size).padder()
    da14d88f265df4cf00b5d11f45559cb8 = f28c2c1585824cc28d5bc045cf4c5b13.update(aa9eddcb39de50597424b155a6f7e043.encode()) + f28c2c1585824cc28d5bc045cf4c5b13.finalize()
    b0f60951a89178a9b6de18836b6b8a74 = f8c2fea25e65a76d7339129e17164c40.encryptor()
    c5ce990ad72721c6cfe88ae681f89257 = b0f60951a89178a9b6de18836b6b8a74.update(da14d88f265df4cf00b5d11f45559cb8) + b0f60951a89178a9b6de18836b6b8a74.finalize()
    ee74d0d93403de6a244a6c150e8bff41 = base64.b64encode(a84b32590693190747d6019b6b735ac1 + c5ce990ad72721c6cfe88ae681f89257).decode()
    return ee74d0d93403de6a244a6c150e8bff41




#The output has been intercepted: z64UqHzDyEcZ577MyryIoSpNYdLeOjvA5wrE1bHNagVcDWoHMJsmzq2W6+Ug76vOWIJln2ujWW4KQ/7rUDFWhw==

```

## Steps to Solve


1. **Collect hints available**:

   Although all the variable names have been hashed to make unreadable, you can still get some information about what this function does.
   The interesting things are:
   - The imports clearly hint to this being a encryption algorithm.
   - The code shows that AES algorithm is used -> the encryption is symmetrical and can be undone with the key
   - When looking at how the Cipher library works, one may notice that the key for the encrytion is hardcoded inside the function as the `f4382049c37f07c9d8ae892efd792247` variable

2. **Write a implementation that reverses AES encrytion**:

  Now that you have the key and the output figured out, you can write a function to reverse the AES encrytion (or use AI or some other resources).
  it looks something like this:
  ```py
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
  ```
   

## Conclusion

It is a fun little challange where you can learn to analyze code even it is obscured.
