import random
from django.shortcuts import redirect, render
from django.urls import reverse
from . import util
from django import forms
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.index()
       
    })

def CreateNewPage(request):
    if request.method == "POST":
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            entries = [entry.upper() for entry in util.list_entries()]
            if title.upper() in entries:
                return render(request, "encyclopedia/CreatError.html")                 
            else:
                content = form.cleaned_data["content"]
            util.save_entry(title, content)
            mdconverted = util.convert_markdown_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "mdtitle": title.upper(),
                "mdconverted": mdconverted,
                "entries": util.index()         
            })           
    else:
        form = CreateNewPageForm()
    
    return render(request, "encyclopedia/CreateNewPage.html", {"form": form})
        

def entry(request, title):
    entries = [entry.upper() for entry in util.list_entries()]
    
    if title.upper() in entries:
        
        mdconverted = util.convert_markdown_to_html(title)
    
        return render(request, "encyclopedia/entry.html", {
            "mdconverted": mdconverted,
            "mdtitle" : title.upper(),
            "entries": util.index()
    })
    
    if title.upper() not in entries:
        return render(request, "encyclopedia/error.html", {"entries": entries})
    

def SearchSuggestion(query):
    entries = util.list_entries()
    suggestions = [entry for entry in entries if query.upper() in entry.upper()]
    return suggestions

    
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

            suggestions = SearchSuggestion(search_query)
            suggestions = [suggestion.upper() for suggestion in suggestions]
            
            return render(request, "encyclopedia/search.html",{
                "entries": util.index(),
                "suggestions" : suggestions
            })

        return render(request, "encyclopedia/entry.html", {
            "mdconverted": util.convert_markdown_to_html(matched_entry),
            "mdtitle": matched_entry,
            "entries": util.index()
            })
    
def WikiTour(request):

    choice = util.list_entries()

    title = random.choice(choice)

    mdconverted = util.convert_markdown_to_html(title)
    return entry(request, title)

def Edit(request, title):
    initial_data = {
        'title': title,
        'content': util.get_entry(title)  
    }

    form = CreateNewPageForm(initial=initial_data)
    return render(request, 'encyclopedia/edit.html', {'title': title, 'form': form})



def Save(request, title):
    if request.method == 'POST':
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            
   
            return redirect('entry', title=title)
        else:

            pass
    


class CreateNewPageForm(forms.Form):
    title = forms.CharField(label='', widget=forms.Textarea(attrs={"rows":1, "cols":100, "placeholder":'Title'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={"rows":25, "cols":100, "placeholder":'Type new content here'}))



