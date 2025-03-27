# Solana Assets

Web challenge where you must retrieve the flag from a cookie that contains it.  
**Level**: Easy

## Challenge Overview:

  - The attacker needs to retrieve a flag from a web application. The flag is stored in a cookie named `flag`, but it is dynamically generated. The attacker must perform specific actions within the web application to gain access to the flag stored in the cookie.

  - The challenge includes typical security protections, such as HTTP-only cookies and obfuscation, which the attacker must bypass.

---

## Application Structure

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
      - CHALLENGEKEY=CTF_CHALLENGE_2023
```

### Directory Structure

```
Solana_Assets/
├── django/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── manage.py
│       ├── SolanaAssets/
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       └── Solana/
│           ├── __init__.py
│           ├── admin.py
│           ├── apps.py
│           ├── models.py
│           ├── urls.py
│           ├── views.py
│           └── templates/
│               └── Solana/
│                   ├── index.html
│                   ├── dashboard.html
│                   ├── news.html
│                   ├── files.html
│                   └── wrong.html
├── docker-compose.yml
└── README.md
```

## Web Application:

The application is a simple Django web app with multiple pages:

- **Login Page** (`/`): Users can log in with specific credentials.
- **Dashboard Page** (`/dashboard`): Once logged in, users are directed to the dashboard where they can view their crypto assets.
- **News Page** (`/news`): Contains latest cryptocurrency news.
- **Files Page** (`/files`): Contains wallet credentials.
- **Wrong Page** (`/right`): A misleading page with a troll message.

### Authentication Flow

```python
def index(request):
    # Clear any existing session
    request.session.flush()
    
    # Clear any existing cookies
    response = render(request, "Solana/index.html")
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    
    # Set a decoy cookie
    response.set_cookie("Gemma-Lehre", "Its not that easy buddy")
    return response

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Check for valid credentials
        if username == "Andreas" and password == "GoodPassw0rd123":
            request.session["is_authenticated"] = True
            return redirect("dashboard")
        elif username == "Leon" and password == "Admin123":
            response = render(request, "Solana/wrong.html")
            response.set_cookie("Flag", "FF{try /files}")
            return response
        else:
            return redirect("index")
    return redirect("index")
```

### Cookie Properties:

The `Flag` cookie has the following properties:
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

### Other Routes

```python
def news(request):
    response = render(request, "Solana/news.html")
    return response

def files(request):
    response = render(request, "Solana/files.html")
    return response

def wrong(request):
    response = render(request, "Solana/wrong.html")
    response.set_cookie("Flag", "FF{try /files}")
    return response
```

## Challenge Mechanics

The challenge involves several key mechanics:

1. **Authentication Bypass**: The dashboard page sets the actual flag cookie regardless of authentication, so direct access to `/dashboard` can bypass authentication checks.

2. **Multiple Routes**: Different routes provide hints or partial information:
   - `/files` reveals valid login credentials
   - `/right` is a misleading route that sets a fake flag

3. **Flag Generation**: The real flag is dynamically generated by combining:
   - The team-specific key (environment variable `TEAMKEY`)
   - The challenge key (environment variable `CHALLENGEKEY`)
   - Then hashing with SHA-256 and formatting as `FF{hash}`

## Technical guideline

### Installation

> [!NOTE]
> Make sure to install docker and docker-compose first

**Linux**

- [Docker Linux installation](https://docs.docker.com/engine/install/ubuntu/)

- [Docker-compose Linux installation](https://docs.docker.com/compose/install/linux/)

**Windows**

- [Docker Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)

- [Docker-compose Windows installation](https://docs.docker.com/compose/install/)

After installing Docker and Docker Compose, pull the repository via the CLI using the following command:

```
git clone https://github.com/CTF-FlagFrenzy/challenges.git
```

Then you navigate to the root of the `Solana Assets` challenge and type the following command in the CLI:

```
docker-compose up
```

Now you can see all running containers with `docker ps`.

### Accessing the Challenge

1. Open your browser and navigate to `http://localhost:8000/`
2. The application should be running and ready for the challenge

### Solution Approach

1. Explore the various endpoints of the application
2. Navigate directly to `/dashboard` to bypass authentication
3. Inspect the cookies to find the `Flag` cookie with the dynamically generated flag
4. Submit the flag in the format `FF{hash_value}`

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Solana_Assets/writeup.md)



