# models.py
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    flag = models.CharField(max_length=64, blank=True, null=True)
