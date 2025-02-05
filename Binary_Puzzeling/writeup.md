# Checking Encryption

A challenge that provides the user with a file (or depending on the browser just text), the problem is that the output looks nonsensical
````
.CA	YV
AAF_YJK@FXVSDSA]
V_

	BWhat might this string be doing?????
```
The "What might this string be doing????" is always the same, the part before it is the flag. It was XOR'ed with the "what might this string be doing????". It can be reversed by converting everything into binary and XOR'ing it again. 
The algorithm might look something like this:

```py
def xor_strings(s1, s2):
    # Ensure the strings are of the same length
    if len(s1) != len(s2):
        raise ValueError("Strings must be of the same length")
    
    # Convert strings to binary and XOR them
    xor_result = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))
    
    return xor_result
```