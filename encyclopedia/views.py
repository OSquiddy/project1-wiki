from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.views.defaults import page_not_found
from markdown2 import markdown_path, Markdown
from django import forms
import random

from . import util

class SearchForm(forms.Form):
    title = forms.CharField()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })    

def entry(request, entryName):
    print(entryName)
    print(util.list_entries())
    information = util.get_entry(entryName)
    if information == None:
        return render(request, "encyclopedia/404.html")
    html = markdown_path(f"entries/{entryName}.md")
    return render(request, f"encyclopedia/entry.html", {
        "info" : html,
        "title" : entryName.capitalize()
    }) 
    

def new_search(request):
    print(request.GET) 
    print(request.GET['q'])
    query = request.GET['q'].lower()
    entryList = util.list_entries()
    resultList = []
    for entry in entryList:
        if query == entry.lower():
            html = markdown_path(f"entries/{query}.md")
            return render(request, f"encyclopedia/entry.html", {
                "info" : html,
                "title" : query.capitalize()
            })
        elif query in entry.lower():
            resultList.append(entry)
    print(resultList)
    if len(resultList) == 0:
        return render(request, "encyclopedia/404.html")        
    else:
        return render(request, "encyclopedia/search.html", {
            "entries" : resultList,
            "query" : query
        })
    html = markdown_path(f"entries/{request.GET['q']}.md")
    return render(request, f"encyclopedia/entry.html", {
        "info" : html,
        "title" : query.capitalize()
    })

def randomPage(request):
    entryList = util.list_entries()
    randPage = random.choice(entryList)
    print(randPage)
    return redirect(f"/wiki/{randPage}")
