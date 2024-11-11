# The SQL Heist

Web challenge where you have to exploit a search function in order to get the flag **Level**:Easy


## Challenge Overview:

 write some challenge overview

---

### Dockerfile

Starting off with the docker-compose file, this file start the challenge container to use it for the CTF. 

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
      - CHALLENGEKEY=NQ^D@zd$q6
```

### Web Application:

Write 1 or 2 sentences about the code

```html
    <main class="container mx-auto p-4 grid grid-cols-3 gap-4">
        <!-- Articles Section -->
        <section class="col-span-2 scrollable">
            {% for article in articles %}
                <article class="bg-gray-800 p-4 rounded-lg mb-4">
                    <h2 class="text-xl font-bold mb-2">{{ article.title }}</h2>
                    <p class="text-gray-400">{{ article.content }}</p>
                </article>
            {% empty %}
                <p class="text-gray-400">No articles found.</p>
            {% endfor %}
        </section>

        <!-- Breaking News Section -->
        <aside class="bg-gray-800 p-4 rounded-lg scrollable">
            <h2 class="text-xl font-bold shine mb-2">Breaking News</h2>
            <ul class="text-gray-400">
                {% for news in breaking_news %}
                    <li class="fas fa-newspape text-white shine mb-2 glow-red">{{ news.title }}</li>
                {% endfor %}
            </ul>
        </aside>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 p-4 text-center rounded-lg mt-4 w-full fixed bottom-0">
              <p class="text-gray-500">&copy; 2023 Dark News Paper. All rights reserved.</p>
    </footer>

    {% if flag %}
        <div class="fixed bottom-0 right-0 m-4 p-4 bg-red-600 text-white rounded-lg">
            <p><strong>Flag: {{ flag }}</strong></p>
        </div>
    {% endif %}
```


### SQL Injection backend

Write some details about the code below


```python
def index(request):
    query = request.GET.get("q")
    flag = None
    #! This is the flag that you need to get from the environment variables
    teamflag = os.environ.get("TEAMKEY")
    challengeflag = os.environ.get("CHALLENGEKEY")
    combined_flag = challengeflag + teamflag
    hashed_flag = hashlib.sha256(combined_flag.encode()).hexdigest()

    articles = []
    if query:
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM The_SQL_Heist_App_article WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"
            )
            rows = cursor.fetchall()
            for row in rows:
                articles.append({"title": row[1], "content": row[2]})
            if "flag" in query:
                flag = f"FF{{{hashed_flag}}}"
    else:
        articles = Article.objects.all()

    breaking_news = random.sample(list(Article.objects.all()), 5)

    return render(
        request,
        "SQL_Heist/index.html",
        {"articles": articles, "flag": flag, "breaking_news": breaking_news},
    )
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
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/The_SQL_Heist/writeup/writeup.md)