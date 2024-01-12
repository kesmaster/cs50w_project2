from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.error, name="error"),
    path("addentryerror", views.addentryerror, name="addentryerror"),
    path("add", views.add, name="add"),
    path("search", views.search, name="search"),
    path("randomentry", views.randomentry, name="randomentry"),
    path("<str:name>", views.entry, name="entry"),
    path("edit/<str:name>", views.edit, name="edit"),
    
]
