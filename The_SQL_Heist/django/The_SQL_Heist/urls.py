from django.urls import include, path

urlpatterns = [
    path(
        "", include("The_SQL_Heist_App.urls")
    ),  # Ändern Sie dies, um die App-URLs in der Root-URL zu haben
]
