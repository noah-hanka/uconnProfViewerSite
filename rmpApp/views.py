from django.http import HttpResponse
from django.template import loader
from rmpApp.query import rmp

uconn_id = 'U2Nob29sLTEwOTE='
uconnRMP = rmp(uconn_id)

selectedTeachers = []
selectedTeachersDict = dict()
teacherReviewDict = dict()

def home(request):
    global selectedTeachers
    selectedTeachers = []
    if (request.method == 'POST'):
        selectedTeachers = request.POST['teacherData'].split(',')
    template = loader.get_template('rmpApp/home.html')
    global selectedTeachersDict
    selectedTeachersDict = dict()
    global teacherReviewDict
    teacherReviewDict = dict()
    for teacher in selectedTeachers:
        teacherParts = teacher.split('_')
        tid = teacherParts[-1]
        legacyId = teacherParts[-2]
        teacherData = uconnRMP.fetchProfData(legacyId,tid)
        teacherReviewDict[teacher] = teacherData
        selectedTeachersDict[teacher] = teacherData['professor']
    print(teacherReviewDict[list(teacherReviewDict.keys())[0]]['reviews'][0].keys())
    context = {
        'teacherList':selectedTeachers,
        'teacherDict':selectedTeachersDict,
        'teacherReviewDict':teacherReviewDict
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
    global selectedTeachersDict
    context = {
        'searchResults':searchResults,
        'noResults':noResults,
        'allResultsShown':allResultsShown,
        'searchQuery':searchQuery,
        'searchResultsNames':searchResultsNames,
        'selectedTeachers':selectedTeachers,
        'selectedTeachersJsonList':{'list':selectedTeachers},
        'selectedTeachersDict':selectedTeachersDict
    }
    context.update(teacherLookupKey)

    return HttpResponse(template.render(context,request))