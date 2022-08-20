from django.http import HttpResponse
from django.template import loader
from rmpApp.query import rmp

uconn_id = 'U2Nob29sLTEwOTE='
uconnRMP = rmp(uconn_id)

selectedTeachers = []

def home(request):
    template = loader.get_template('rmpApp/home.html')
    context = {
    }
    return HttpResponse(template.render(context,request))

def search(request):
    searchQuery = request.GET["search"]
    noResults = False

    allResultsShown = False



    searchResults = uconnRMP.search(searchQuery)
    if len(searchResults) <= 20: allResultsShown = True
    searchResultsNames = list(searchResults.keys())[:20]

    if len(searchResults) == 0: noResults = True
    template = loader.get_template('rmpApp/search.html')

    for name in searchResultsNames:
        searchResults[name]["firstName"] = searchResults[name]["firstName"].lower()
        searchResults[name]["lastName"] = searchResults[name]["lastName"].lower()        

    teacherLookupKey = {key:key for key in list(list(searchResults.values())[0].keys())} if len(searchResults) > 0 else dict()
    context = {
        'searchResults':searchResults,
        'noResults':noResults,
        'allResultsShown':allResultsShown,
        'searchQuery':searchQuery,
        'searchResultsNames':searchResultsNames,
    }
    context.update(teacherLookupKey)

    return HttpResponse(template.render(context,request))