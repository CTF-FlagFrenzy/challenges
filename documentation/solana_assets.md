# Solana Assest

Web challenge where you have to get the flag with an cookie which contains a flag **Level**:Easy


## Challenge Overview:

  - The attacker needs to retrieve a flag from a web application. The flag is stored in a cookie named flag, but it is dynamically generated. The attacker has to perform actions on the web application to get access to the flag stored in the cookie.

  - The challenge includes typical security protections, like HTTP-only cookies or obfuscation, that the attacker needs to bypass.

---

### Dockerfile

Starting off with the docker-compose file, this file start the challenge container to use it for the CTF, 

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
  Login Page (/login): Users can log in with a specific username (admin) and password.
  Dashboard Page (/dashboard): Once logged in, users are directed to the dashboard, andacookie named flag is set. The cookie contains the dynamically generated flag, but it'snotimmediately accessible through client-side JavaScript (i.e., it's set as HTTP-only).

### Cookie Properties:

  The flag cookie should have the following properties:
  HTTP-only: Prevents access to the flag via JavaScript.
  Secure: Ensures that the cookie is only sent over HTTPS.
  Dynamic: The flag is unique per session, generated during the login process.

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

After you installed docker and docker-compose you need to pull the repository via cli using this command.

```
git pull https://github.com/CTF-FlagFrenzy/challenges.git
```

Then you navigate to the root of the `Solana Assests` challenge and type the following command in the cli.

```
docker-compose up
```

You can see all running container with `docker ps`.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Solana_Assets/writeup/writeup.md)



