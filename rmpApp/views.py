from django.http import HttpResponse
from django.template import loader
from rmpApp.query import rmp

uconn_id = 'U2Nob29sLTEwOTE='
uconnRMP = rmp(uconn_id)

# for testing purposes
selectedTeachers = ['A_Deener_1395977']
selectTeachersDict = {'A_Deener_1395977':{'__typename': 'Teacher', 'id': 'VGVhY2hlci0xMzk1OTc3', 'legacyId': 1395977, 'avgRating': 3.8, 'numRatings': 4, 'wouldTakeAgainPercent': 100, 'avgDifficulty': 3.3, 'department': 'Sociology', 'school': {'__ref': 'U2Nob29sLTEwOTE='}, 'firstName': 'A', 'lastName': 'Deener', 'isSaved': False}}

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

    teacherLookupKey = {key:key for key in list(list(searchResults.values())[0].keys())} if len(searchResults) > 0 else dict()
    context = {
        'searchResults':searchResults,
        'noResults':noResults,
        'allResultsShown':allResultsShown,
        'searchQuery':searchQuery,
        'searchResultsNames':searchResultsNames,
        'selectedTeachers':selectedTeachers,
        'selectedTeachersJsonList':{'list':selectedTeachers},
        'selectedTeachersDict':selectTeachersDict
    }
    context.update(teacherLookupKey)

    return HttpResponse(template.render(context,request))