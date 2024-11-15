# CTF Web-Challenge | Shadow_File Writeup: Hard

## Challenge Overview

  - This is a new website created by some students from HTL Mössingerstraße. Use a Linux tool to find a hidden file. The file contains information about cryptocurrency, so take a close look. In the "id" section of each cryptocurrency, you will find a part of the flag. These parts are hex-encoded and shuffled. Pay attention to the unit numbers, as they provide a hint on how to assemble the parts correctly.

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

Now you can see a JSON-formatted text. By checking the IDs, you might notice a letter in the second one. Could it be hex-encoded text? Let’s decode it and find out.
```json
   {
            "id": "36373331336333373639627d",
            "name": "Blockchain T-Shirt",
            "description": "Show your love for blockchain technology with this stylish t-shirt.",
            "picture": "/static/img/products/blockchain_tshirt.png",
            "priceUsd": {
                "currencyCode": "USD",
                "units": 8
            },
            "categories": [
                "crypto",
                "apparel"
            ]
        },
        {
            "id": "65316430316362",
            "name": "Crypto Miner Air Freshener",
            "description": "Keep your mining rig smelling fresh with this air freshener.",
            "picture": "/static/img/products/crypto_miner_air_freshener.png",
            "priceUsd": {
                "currencyCode": "USD",
                "units": 6
            },
            "categories": [
                "crypto",
                "accessories"
            ]
        },
```
4. **Using [Cyberchef](https://cyberchef.io/) you can get new informations**
- **Settings:** From Hex with `None` as delimiter


- Input: `32313738303139383932347d`

- Output: `21780198924}`

Checking the output you see the `{`

By repeating the same process for all other IDs, you can decode all parts of the flag. To assemble the flag in the correct order, take a close look at the "units" field of each product. This field provides the sequence in which the decoded parts need to be arranged to form the correct flag.

`FF{5b6ffc6b2fa2e4a92d5d3ca65116f5fbbb02b5fe1d01cbb5df89967313c3769b}`
