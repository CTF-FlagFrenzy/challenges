# CTF Web-Challenge | Solana Assests Writeup: Easy Medium

## Challenge Overview

  - This is a new website created by some students from HTL Mössingerstraße, use a Linux tool to find a hidden file. The file contains some information about crypto take a good look. In the id section of every crypto coin one part of the flag is there.

## Steps to Solve

1. **Use the FUZZ tool on Linux**:

```sh
ffuf -w common.txt -u http://172.20.18.53:8003/FUZZ > output.txt
 /'___\  /'___\           /'___\                           
/\ \__/ /\ \__/  __  __  /\ \__/    
\ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\   
 \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/ 
  \ \_\   \ \_\  \ \____/  \ \_\   
   \/_/    \/_/   \/___/    \/_/      
                                                           
       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://172.20.18.53:8003/FUZZ
 :: Wordlist         : FUZZ: /home/kali/Documents/wordlists/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________
```

2. **Checking the output.txt file**

You can see that the scan found something `security.txt`

3. **Use the information and get to the txt file**

`http://172.20.18.53:8003/security.txt`

Now you can see a json like formatted text. Checking the ids you can se the flag format FF{}, maybe someone divided the flag in multiple parts... Take the parts and stick them together.
```json
{
            "id": "FF{082f",
            "name": "Bitcoin Paper Wallet (pack of 20)",
            "description": "Securely store your Bitcoin with these paper wallets.",
            "picture": "/static/img/products/bitcoin_paper_wallet.png",
            "priceUsd": {
                "currencyCode": "USD",
                "units": 50
            },
            "categories": [
                "crypto",
                "security"
            ]
        },

{
            "id": "b010771",
            "name": "Ethereum Hardware Wallet",
            "description": "Keep your Ethereum safe with this hardware wallet.",
            "picture": "/static/img/products/ethereum_hardware_wallet.png",
            "priceUsd": {
                "currencyCode": "USD",
                "units": 100
            },
            "categories": [
                "crypto",
                "security"
            ]
        },
```
