from django.urls import path

from . import views

app_name = "page"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryName>", views.entry, name="entry"),
    # path("?q=<str:page_name>", views.search, name="search")
    path("search/", views.new_search, name="search"),
    path("r", views.randomPage, name="random"),
    path("create", views.createPage, name="create"),
    path("wiki/<str:entryName>/edit", views.editPage, name="edit"),
    path("wiki/<str:entryName>/d", views.deleteEntry, name="delete")
]
