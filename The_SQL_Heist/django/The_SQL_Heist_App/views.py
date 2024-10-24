import logging

from django.shortcuts import render

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def index(request):
    response = render(request, "SQL_Heist/index.html")
    return response
