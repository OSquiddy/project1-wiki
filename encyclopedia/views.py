from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.views.defaults import page_not_found
from markdown2 import markdown_path, Markdown
from django import forms
from django.core.files import File
import random

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body", widget=forms.Textarea)

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
    return redirect(f"/wiki/{randPage.lower()}")

def createPage(request):
    status= 0
    if request.method == "POST":
        print(request.POST)
        form = EntryForm(request.POST)
        if form.is_valid():
            if util.get_entry(request.POST['title']) is None:
                status = 1
                util.save_entry(request.POST['title'], request.POST['body'])
                return render(request, f"encyclopedia/createEntry.html", {
                    "status" : status
                })
            else:
                status = 2
                return render(request, f"encyclopedia/createEntry.html", {
                    "status" : status
                })
    return render(request, f"encyclopedia/createEntry.html", {
        "form" : EntryForm(),
        "status" : status
    })

def editPage(request, entryName):
    print(request.POST)
    status = 0
    title = entryName
    body = util.get_entry(entryName)
    data = { "title" : title.capitalize(), "body" : body}
    if request.method == "POST":
        form = EntryForm(data)
        if request.POST.get("save") != None:
            if form.is_valid():
                util.save_entry(request.POST['title'], request.POST['body'])
                html = markdown_path(f"entries/{entryName}.md")
                return render(request, f"encyclopedia/entry.html", {
                    "info" : html,
                    "title" : entryName.capitalize()
                })
        elif request.POST.get("delete") != None:
            if form.is_valid():
                status = 1
                util.delete_entry(request.POST['title'])
                return render(request, f"encyclopedia/editEntry.html", {
                    "form" : form,
                    "status" : status,
                    "Title" : entryName.capitalize()
                })
    return render(request, f"encyclopedia/editEntry.html", {
        "form" : EntryForm(data),
        "status" : status,
        "Title" : entryName.capitalize()
    })

def deleteEntry(request, entryName):
    util.delete_entry(entryName)
    status = 1
    return render(request, f"encyclopedia/editEntry.html", {
        "status" : status,
        "Title" : entryName.capitalize()
    })