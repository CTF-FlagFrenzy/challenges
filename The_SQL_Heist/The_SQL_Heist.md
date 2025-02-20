# The SQL Heist

Web challenge where you have to exploit a search function to retrieve the flag.  
**Level**: Easy



## Challenge Overview:

 The SQL Heist challenge revolves around exploiting a vulnerable search functionality within a web application to retrieve sensitive data. 
 The web app allows users to search for articles using a query, but the query is directly inserted into an SQL statement without proper sanitization, 
 making it susceptible to SQL injection attacks.
 The challenge focuses on understanding and exploiting SQL injection vulnerabilities to gain unauthorized access to the flag stored within the system.

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
```

### Web Application:

This HTML code defines a layout for displaying articles and breaking news in a grid format, with a footer that remains fixed at the bottom of the page. If a flag is set, it is displayed in a fixed position at the bottom-right of the screen.


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


### SQL Injection Backend Overview

The code provided demonstrates a potential vulnerability related to **SQL injection**. It handles a user search query to fetch articles from a database. Here's an analysis of the code and the security concerns:

```python
def index(request):
    query = request.GET.get("q")  # Retrieves the search query from the GET request
    flag = None
    # The flag is retrieved from environment variables and is dynamically generated
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
            if "flag" in query:  # If the query contains the word 'flag', it will show the flag
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
> If you have any problems solving this challenge you can find a full guide [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/The_SQL_Heist/writeup.md)