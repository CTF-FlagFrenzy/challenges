# Checking Encryption

A challenge that provides the user with a file (or depending on the browser just text) that includes a text like `FF{ľad0Ħe5aĭ709Ð844Ñ84dĴ6a9Ĳb88ć263Ę` This looks almost like a flag and the challenge is to reverse this into the correct string.
It uses a custom algorithm that has a variable to define a sum of numbers, for example 4. When it is 4, converts the characters to integers according to the `chr()` and `ord()` functions. Then it sums them together and replaces the last letter with the sum of all the letters. 
So with the input `FF{6` ...
```
F - 70
F - 70
{ - 123
6 - 54 

70+70+123+54 = 317

#Results in
F - 70
F - 70
{ - 123
Ľ - 317
```

This can be revesed using the following algorithm

```py
def undoChecksumming(message, checksum_interval=4):
    if(checksum_interval < 1):
        print("Checksum interval must be at least 2")
        return
    result_message = ""
    charIdx = 1
    for char in message:
        chached_char = char
        if charIdx % checksum_interval == 0:
            #get unicode sum of the current and the characters before according to the checksum_interval
            sum = getStringUnicodeSum(char) - getStringUnicodeSum(message[charIdx-checksum_interval:charIdx-1])
            #convert unicode to char
            chached_char = chr(sum)
        charIdx += 1
        result_message += chached_char
    return result_message
```