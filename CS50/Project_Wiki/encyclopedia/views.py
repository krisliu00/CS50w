import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from django import forms
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
       
    })

def CreateNewPage(request):
    if request.method == "POST":
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/CreateNewPage.html", {
                "form": form
            })

    return render(request, "encyclopedia/CreateNewPage.html",{
        "entries": util.list_entries(),
        "form": CreateNewPageForm()
        
    })  

def entry(request, title):
    
    entries = [entry.upper() for entry in util.list_entries()]
    
    if title.upper() in entries:

        mdconverted = util.convert_markdown_to_html(title)
    
        return render(request, "encyclopedia/entry.html", {
            "mdconverted": mdconverted,
            "mdtitle" : title.upper(),
            "entries": util.list_entries()
    })
    
    if title.upper() not in entries:
        return render(request, "encyclopedia/error.html", {"entries": entries})
    
def search(request):
    if request.method == "GET":
 
        search_query  = request.GET.get('q')
        entries = util.list_entries()

        matched_entry = None
        for entry in entries:
            if search_query.upper() == entry.upper():
                matched_entry = entry
                break

        if matched_entry is None:
            
            return render(request, "encyclopedia/error.html",{"entries": util.list_entries()
                            })

        return render(request, "encyclopedia/search.html", {
            "search_result": util.convert_markdown_to_html(matched_entry),
            "search_title": matched_entry,
            "entries": util.list_entries()
            })
    
def WikiTour(request):

    choice = util.list_entries()

    title = random.choice(choice)

    mdconverted = util.convert_markdown_to_html(title)
    return entry(request, title)
        
      



class CreateNewPageForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={"rows":1, "cols":70, "placeholder":'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":25, "cols":70, "placeholder":'Type new content here'}))


