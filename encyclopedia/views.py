from django.shortcuts import render, redirect
from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_entry_page(request, entry):
    content = util.get_entry(entry)
    
    if content == None:
        return render(request, "encyclopedia/error_page.html", {
            "entry": entry
        })  
    
    html_content = markdown2.markdown(content)
    
    return render(request, "encyclopedia/entry_page.html", {
        "entry": entry,
        "content":  html_content
    })

def search(request):
    query = request.GET.get('q', '').strip() # Gets the value associeted with the key 'q'; the second argument ' ' is the default value
    if not query: #if the questy is empty, redirect to the index page
        return redirect('encyclopedia:index')
    
    # Try to get the exact entry
    content = util.get_entry(query)
    
    if content:   # checks whether 'content' is not None
        # If the entry exists, render the entry page
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry_page.html", {
            "entry": query,
            "content": html_content
        })
    else:
        # If no exact match, find all entries containing the query as a substring
        all_entries = util.list_entries()
        matching_entries = [entry for entry in all_entries if query.lower() in entry.lower()]

        # Render the search results page with matching entries
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "matching_entries": matching_entries
        })
    
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        
        if title in util.list_entries():
            return render(request, "encyclopedia/new_page.html", {
                "error_message": "An entry with this title already exists. Please change the title and / or content.",
                "title": title,
                "content": content
            })
        
        util.save_entry(title, content)
        return redirect('encyclopedia:show_entry_page', entry=title)
    
    return render(request, "encyclopedia/new_page.html")    