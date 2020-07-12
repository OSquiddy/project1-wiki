from django.urls import path

from . import views

app_name = "page"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryName>", views.entry, name="entry"),
    # path("?q=<str:page_name>", views.search, name="search")
    path("wiki/", views.new_search, name="search")
]
