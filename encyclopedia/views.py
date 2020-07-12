from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.views.defaults import page_not_found
from markdown2 import markdown_path, Markdown
from django import forms

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
    return render(request, f"encyclopedia/{entryName}.html", {
        "info" : information
    }) 
    

def new_search(request):
    print(request.GET.__getitem__('q'))
    information = util.get_entry(request.GET.__getitem__('q'))
    print(information)
    if information == None:
        return render(request, "encyclopedia/404.html")
    html = markdown_path(f"entries/{request.GET.__getitem__('q')}.md")
    return render(request, f"encyclopedia/{request.GET.__getitem__('q')}.html", {
        "info" : information
    })


# def handler_404(request, exception):
#     return page_not_found(request, exception, template_name="encyclopedia/404.html")
