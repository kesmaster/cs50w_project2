from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from . import util
from django.shortcuts import redirect
import random

import markdown2

class title_and_content_form(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea, label="Description")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def add(request):

    if request.method == "POST":
        form = title_and_content_form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["description"]
            # check if exists
            if util.get_entry(title) == None:
                # if it does exist save
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "content": markdown2.markdown(util.get_entry(title)),
                    "title": title
                    })

            else:
                return render(request, "encyclopedia/addentryerror.html", {
                    "name": title
                })
    else:

        form = title_and_content_form()

    return render(request, "encyclopedia/addentry.html", {"form": form})


def addentryerror(request):
    return render(request, "encyclopedia/addentryerror.html")


def error(request):
    return render(request, "encyclopedia/error.html")


def entry(request, name):
    if util.get_entry(name):
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(util.get_entry(name)),
            "title": name
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "name": name
        })

def search(request):
    if request.method == "GET":
        search_query = request.GET.get('q')
        print(search_query)

        full_list = util.list_entries()
        # Check if search query is in the list
        if search_query in full_list:
            return render(request, "encyclopedia/entry.html", {
                "content": markdown2.markdown(util.get_entry(search_query)),
                "title": search_query
            })
        else:
            list_filtered = list(filter(lambda x: search_query in x, full_list))
            print(list_filtered)
            return render(request, "encyclopedia/index.html", {
                "entries": list_filtered
            })
            
def edit(request, name):
    if request.method == "POST":
        form = title_and_content_form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["description"]
            util.save_entry(title, content)
            # return render(request, "encyclopedia/entry.html", {
            #     "content": markdown2.markdown(util.get_entry(title)),
            #     "title": title
            #     })

            return HttpResponseRedirect(reverse('entry', kwargs={'name': name}))
    else:
        form = title_and_content_form()
        # form.fields['description'].widget.attrs['placeholder']= util.get_entry(name)
        form.fields['title'].initial = name
        form.fields['description'].initial = util.get_entry(name)

    return render(request, "encyclopedia/editentry.html", {
        "form": form,
        "name": name
        })

def randomentry(request):
    list = util.list_entries()
    item = random.choice(list)
    return HttpResponseRedirect(reverse('entry', kwargs={'name': item}))
    # return render(request, "encyclopedia/entry.html", {
    #     "content": markdown2.markdown(util.get_entry(item)),
    #     "title": item
    # })
