import hashlib
import logging
import os

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def index(request):
    trollflag = "Its not that easy buddy"
    hashlib.sha256(trollflag.encode()).hexdigest()
    response = render(request, "Solana/index.html")
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    response.set_cookie("Gemma-Lehre", f"{trollflag}")

    return response


def dashboard(request):
    #! This is the flag that you need to get from the environment variables
    teamflag = os.environ.get("TEAMKEY")
    challengeflag = "R^@LgvG5QD"

    combined_flag = challengeflag + teamflag
    hashed_flag = hashlib.sha256(combined_flag.encode()).hexdigest()

    logging.info(f"Hashed Flag: {hashed_flag}")

    response = render(request, "Solana/dashboard.html")
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    response.set_cookie("Flag", f"FF{{{hashed_flag}}}", max_age=7 * 24 * 60 * 60)

    return response


def news(request):
    return render(request, "Solana/news.html")


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if username == "Andreas" and password == "GoodPassw0rd123":
            return redirect("dashboard")
        if username == "Leon" and password == "Admin123":
            return redirect("wrong")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("index")
    return render(request, "Solana/index.html")


def wrong(request):
    response = render(request, "Solana/wrong.html")
    trollflag2 = "try /files"
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    response.set_cookie("Flag", f"FF{{{trollflag2}}}")
    return response


def files(request):
    response = render(request, "Solana/files.html")
    return response
