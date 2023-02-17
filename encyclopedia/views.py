from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.http import HttpResponse
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Gets the HTML content of the requested page after markdown conversion
def entry(request, title):
    markdowner = Markdown()
    text = markdowner.convert(f"{util.get_entry(title)}")
    if util.get_entry(title):
        return render(request, "encyclopedia/pages.html", {
            "title": title,
            "body": text
        })
    return render(request, "encyclopedia/error.html")


# Searches for a page by title
def search(request):
    if request.method == "POST":
        entry = request.POST.get("q")
        if entry:
            markdowner = Markdown()
            entryPage = markdowner.convert(f"{util.get_entry(entry)}")
            # Gets page, if it exists
            if util.get_entry(entry):
                return render(request, "encyclopedia/pages.html" , {
                    "title": entry,
                    "body": entryPage
                })
      
            # Displays a page containing a list of all the pages whose titles contain the searched query as a substring
            else:
                search_results = []
                entries = util.list_entries()
                for item in entries:
                    if entry.lower() in item.lower():
                        search_results.append(item)
                return render(request, "encyclopedia/search.html", {
                    "results": search_results
                })
                
        else:
            return render(request, "encyclopedia/search.html", {
                "results": util.list_entries()
            })


def create(request):
    if request.method == "POST":
        entries = util.list_entries()
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            return render(request, "encyclopedia/new.html")
        # Prompts the user with a response if a page with same title already exists
        if title in entries:
            return HttpResponse(f"A {title} page already exists!")

        # Otherwise, saves the new entry to disk and displays the new page
        util.save_entry(title, content)
        markdowner = Markdown()
        new_entry = markdowner.convert(f"{util.get_entry(title)}")
        return render(request, "encyclopedia/pages.html", {
            "title": title,
            "body": new_entry
        })
    return render(request, "encyclopedia/new.html")


def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        # Prevents the user from saving empty content after editing
        if not content:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": ""
            })

        # Saves the edited content and displays the updated page
        util.save_entry(title, content)
        markdowner = Markdown()
        new_entry = markdowner.convert(f"{util.get_entry(title)}")
        return render(request, "encyclopedia/pages.html", {
            "title": title,
            "body": new_entry
        })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title)
    })


def randomise(request):
    random_page = random.choice(util.list_entries())
    markdowner = Markdown()
    content = markdowner.convert(f"{util.get_entry(random_page)}")
    return render(request, "encyclopedia/pages.html", {
        "title": random_page,
        "body": content
    })