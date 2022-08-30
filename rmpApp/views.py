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
    if selectedTeachers == ['']:
        selectedTeachers = []
    template = loader.get_template('rmpApp/home.html')
    global selectedTeachersDict
    selectedTeachersDict = dict()
    global teacherReviewDict
    teacherReviewDict = dict()
    print(selectedTeachers)
    for teacher in selectedTeachers:
        teacherParts = teacher.split('_')
        tid = teacherParts[-1]
        legacyId = teacherParts[-2]
        teacherData = uconnRMP.fetchProfData(legacyId,tid)
        teacherReviewDict[teacher] = teacherData
        selectedTeachersDict[teacher] = teacherData['professor']
    context = {
        'teacherList':selectedTeachers,
        'selectedTeachersJsonList':{'list':selectedTeachers},
        'teacherDict':selectedTeachersDict,
        'teacherReviewDict':teacherReviewDict
    }
    print(selectedTeachers)
    return HttpResponse(template.render(context,request))

def search(request):
    global selectedTeachersDict
    global selectedTeachers
    print(request.POST)
    if (request.method == 'POST'):
        searchQuery = request.POST["search"]
        selectedTeachers = request.POST['teacherData'].split(',')

    if selectedTeachers == ['']:
        selectedTeachers = []
    

    newTeacherDict = dict()
    for teacher in selectedTeachers:
        if teacher not in selectedTeachersDict:
            teacherParts = teacher.split('_')
            tid = teacherParts[-1]
            legacyId = teacherParts[-2]
            teacherData = uconnRMP.fetchProfData(legacyId,tid)
            newTeacherDict[teacher] = teacherData['professor']
        else:
            newTeacherDict[teacher] = selectedTeachersDict[teacher]
    selectedTeachersDict = newTeacherDict

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
        'selectedTeachersDict':selectedTeachersDict
    }
    context.update(teacherLookupKey)

    return HttpResponse(template.render(context,request))