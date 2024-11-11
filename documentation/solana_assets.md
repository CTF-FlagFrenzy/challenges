# Solana Assest

Web challenge where you must retrieve the flag from a cookie that contains it.  
**Level**: Easy

## Challenge Overview:

  - The attacker needs to retrieve a flag from a web application. The flag is stored in a cookie named `flag`, but it is dynamically generated. The attacker must perform specific actions within the web application to gain access to the flag stored in the cookie.

  - The challenge includes typical security protections, such as HTTP-only cookies and obfuscation, which the attacker must bypass.


---

### Dockerfile

Starting with the `docker-compose` file, this file starts the challenge container to set up the environment for the CTF.


```yml
version: '3'

volumes:
  my-django-data:

services:
  web:
    build:
      context: .
      dockerfile: django/Dockerfile

    volumes:
      - my-django-data:/media

    working_dir: '/code'

    ports:
      - '8000:8000'

    environment:
      - TEAMKEY=XXXXXXX
      - CHALLENGEKEY=R^@LgvG5QD
```

### Web Application:

A simple web app with two pages:
- **Login Page** (`/login`): Users can log in with a specific username (`admin`) and password.
- **Dashboard Page** (`/dashboard`): Once logged in, users are directed to the dashboard, and a cookie named `flag` is set. This cookie contains the dynamically generated flag, but it is not immediately accessible through client-side JavaScript (as it is set as HTTP-only).


### Cookie Properties:

The `flag` cookie has the following properties:
- **HTTP-only**: Prevents access to the flag via JavaScript.
- **Secure**: Ensures the cookie is only sent over HTTPS.
- **Dynamic**: The flag is unique per session and is generated during the login process.


```python
    def dashboard(request):
        #! This is the flag that you need to get from the environment variables
        teamflag = os.environ.get("TEAMKEY")
        challengeflag = os.environ.get("CHALLENGEKEY")
        if not request.session.get("is_authenticated"):
            return redirect("index")
        
        else:
            combined_flag = challengeflag + teamflag
            hashed_flag = hashlib.sha256(combined_flag.encode()).hexdigest()
            logging.info(f"Hashed Flag: {hashed_flag}")
            response = render(request, "Solana/dashboard.html")
            
            for cookie in request.COOKIES:
                response.delete_cookie(cookie)
            response.set_cookie("Flag", f"FF{{{hashed_flag}}}", max_age=7 * 24 * 60 * 60)
            return response
```

## Technical guideline

### Installation

> [!NOTE]
> Make sure to install docker and docker-compose first

**Linux**

- [Docker Linux installation](https://docs.docker.com/engine/install/ubuntu/)

- [Docker-compose Linux installation](https://docs.docker.com/compose/install/linux/)

**Windwos**

- [Docker Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)

- [Docker-compose Windows installation](https://docs.docker.com/compose/install/)

After installing Docker and Docker Compose, pull the repository via the CLI using the following command:



```
git pull https://github.com/CTF-FlagFrenzy/challenges.git
```

Then you navigate to the root of the `Solana Assests` challenge and type the following command in the cli.

```
docker-compose up
```

Now you can see all running container with `docker ps`.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Solana_Assets/writeup/writeup.md)



