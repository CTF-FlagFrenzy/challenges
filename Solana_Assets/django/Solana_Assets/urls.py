from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "", include("Solana_Assets_App.urls")
    ),  # Ändern Sie dies, um die App-URLs in der Root-URL zu haben
]
