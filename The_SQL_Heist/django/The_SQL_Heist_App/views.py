import hashlib
import logging
import os
import random

from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse

from .models import Article

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def index(request):
    query = request.GET.get("q")
    flag = None
    teamflag = os.environ.get("TEAMKEY", "TEAMKEY")
    challengeflag = os.environ.get("CHALLENGEKEY", "CHALLENGEKEY")
    combined_flag = challengeflag + teamflag
    hashed_flag = hashlib.sha256(combined_flag.encode()).hexdigest()
    flag_value = f"FF{{{hashed_flag}}}"

    existing_article = Article.objects.filter(flag=flag_value).first()
    if existing_article:
        existing_article.delete()
        logging.info("Existing article with flag deleted.")

    Article.objects.create(
        title="Special Article",
        content="This article contains the flag.",
        flag=flag_value
    )
    logging.info("Article with flag created.")

    articles = []
    if query:
        if "flag" in query.lower(): 
            # Generate a single popup with a skull
            popup_script = """
            <script>
                alert('Its not that easy buddy 💀');
                window.location.href='/';
            </script>
            """
            return HttpResponse(popup_script)
        with connection.cursor() as cursor:
            # SQL injection vulnerability
            sql_query = f"SELECT * FROM The_SQL_Heist_App_article WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"
            logging.info(f"Executing SQL query: {sql_query}")
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            for row in rows:
                articles.append({"title": row[1], "content": row[2]})
                if row[3]: # Check if flag is set
                    flag = row[3]
    else:
        articles = Article.objects.all()

    breaking_news = random.sample(list(Article.objects.all()), 5)

    return render(
        request,
        "SQL_Heist/index.html",
        {"articles": articles, "flag": flag, "breaking_news": breaking_news},
    )