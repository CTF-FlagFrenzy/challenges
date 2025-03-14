# CTF-Challange | PYCked Apart writeup: Level Easy
> _This challenge is called `PYCked Apart`, but you may also see it referred to as it's working name `Pydetect` in some places._

## Challange Overview
In this challange the user is provided a compiled python script and a flag file, the goal is it to decompile the provided script, find out how the flag is stored and write a script to reverse this process and extract the flag from it's file

## Steps to Solve

1. **Decompilation**\
  An easy option to decompile the Python script is [pycdc](https://github.com/zrax/pycdc). Precompiled binaries for Linux and Windows are available to [download here](https://github.com/extremecoders-re/decompyle-builds/releases), use them to decompile the Python script.
    ```sh
    chmod +x ./pycdc.x86_64 # Make file executable on Linux
    ./pycdc.x86_64 encoder.py > decompiled.py
    ```
    ```py
    # Source Generated with Decompyle++
    # File: encoder.pyc (Python 3.7)

    import pickle
    import zlib
    from base64 import urlsafe_b64encode as b64enc
    flag = open('flag.txt', 'r').read()
    enc = b64enc(zlib.compress(bytes(flag, 'utf-8')))
    with open('flag', 'wb') as f:
        pickle.dump(enc, f)
    ```

2. **Analyzing the encoder**\
  You can see, the flag is stored in a pickle file as a Base64 encoded, zlib compressed bytes object.

3. **Reverse and exrtract the Flag**\
  The steps to reverse this process are:
    1. Importing all the required Python Libraries
    ```py
    import zlib
    import pickle
    from base64 import urlsafe_b64decode as b64dec
    ```

    2. Loading the flag file with [`pickle.load()`](https://docs.python.org/3.11/library/pickle.html#pickle.load)
    ```py
    with open('flag', 'rb') as f:
        data = pickle.load(f)
    ```

    3. Decode the base64 String using [`base64.urlsafe_b64decode()`](https://docs.python.org/3.11/library/base64.html#base64.urlsafe_b64decode) 
    >_In this example `base64.urlsafe_b64decode` is imported as `b64dec`, so this will be used_
    ```py
        compressed_flag = b64dec(data)
    ```

    4. Decompress the flag with [`zlib.decompress()`](https://docs.python.org/3.11/library/zlib.html#zlib.decompress)
    ```py
        flag = zlib.decompress(compressed_flag)
    ```

    5. Print out the flag
    ```py
        print(flag)
    ```
  
    The file decoder should look something like this:
    ```py
    import zlib
    import pickle
    from base64 import urlsafe_b64decode as b64dec

    with open('flag', 'rb') as f:
        data = pickle.load(f)
    
        compressed_flag = b64dec(data)
        flag = zlib.decompress(compressed_flag)
        print(flag)
    ```

    running this will give you the flag as a bytes object, however it does not need to be converted to a string.
    >_use `python3` if you are on Linux, and `py` if you are on Windows_
    ```sh
    python3 decoder.py 
    b'FF{e0aa71973d5c4703ef39648833eb8c8925fbec02edc52b7a2944ad9830b22dac}'
    ```
