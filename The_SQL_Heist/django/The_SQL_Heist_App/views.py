import logging
from django.db import connection
from .models import Article
from django.shortcuts import render
import hashlib
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def index(request):
    query = request.GET.get('q')
    #! This is the flag that you need to get from the environment variables
    # teamflag = os.environ.get('TEAMFLAG')
    flag = None
    teamflag = "teamflag"
    challengeflag = "nkN7FPpuB#"
    combined_flag = challengeflag + teamflag
    hashed_flag = hashlib.sha256(combined_flag.encode()).hexdigest()

    articles = []
    if query:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM The_SQL_Heist_App_article WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'")
            rows = cursor.fetchall()
            for row in rows:
                articles.append({
                    'title': row[1],  # Assuming title is the second column
                    'content': row[2]  # Assuming content is the third column
                })
            # Überprüfen Sie, ob die SQL-Injection erfolgreich war
            if "flag" in query:
                flag = f"FF{{{hashed_flag}}}"
    else:
        articles = Article.objects.all()

    # Get 5 random articles for breaking news
    breaking_news = random.sample(list(Article.objects.all()), 5)

    return render(request, 'SQL_Heist/index.html', {'articles': articles, 'flag': flag, 'breaking_news': breaking_news})