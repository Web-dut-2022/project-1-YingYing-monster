from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:TITLE>", views.entry, name="entry"),
    path("new/", views.newpage, name="newpage"),
    path("edit/<str:TITLE>/", views.editpage, name="editpage"),
    path("random/", views.random, name="random")
]
