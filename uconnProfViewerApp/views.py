from django.http import HttpResponse
from django.template import loader
from uconnProfViewerApp.query import rmp
import time

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
    template = loader.get_template('uconnProfViewerApp/home.html')
    global selectedTeachersDict
    newTeacherDict = dict()
    global teacherReviewDict
    newReviewDict = dict()
    start = time.time()
    for teacher in selectedTeachers:
        if teacher in teacherReviewDict and selectedTeachersDict:
            newReviewDict[teacher] = teacherReviewDict[teacher]
            newTeacherDict[teacher] = selectedTeachersDict[teacher]
        else:
            teacherParts = teacher.split('_')
            tid = teacherParts[-1]
            legacyId = teacherParts[-2]
            teacherData = uconnRMP.fetchProfData(legacyId,tid)
            newReviewDict[teacher] = teacherData
            newTeacherDict[teacher] = teacherData['professor']
    end = time.time()
    print(f'Time to collect teacher reviews : {end-start}')
    selectedTeachersDict = newTeacherDict
    teacherReviewDict = newReviewDict
    # print(teacherReviewDict[list(teacherReviewDict.keys())[0]]['reviews'][12].items())

    #professor, distribution, reviews
    #professor : ['id', 'legacyId', 'firstName', 'lastName', 'lockStatus', 'department', 'isSaved', 'numRatings', 'avgRating', 'isProfCurrentUser', 'avgDifficulty', 'wouldTakeAgainPercent']
    #distribution : ['total', 'r1', 'r2', 'r3', 'r4', 'r5']
    #reviews : list() --> ['comment', 'flagStatus', 'createdByUser', 'teacherNote', 'date', 'class', 'helpfulRating', 'clarityRating', 'isForOnlineClass', 'legacyId', 'difficultyRating', 'attendanceMandatory', 'wouldTakeAgain', 'grade', 'textbookUse', 'isForCredit', 'ratingTags', 'id', 'adminReviewedAt', 'thumbsUpTotal', 'thumbsDownTotal']
    context = {
        'teacherList':selectedTeachers,
        'selectedTeachersJsonList':{'list':selectedTeachers},
        'teacherDict':selectedTeachersDict,
        'teacherReviewDict':teacherReviewDict,
        'teachersExist':(len(selectedTeachers)!=0)
    }
    return HttpResponse(template.render(context,request))

def search(request):
    global selectedTeachersDict
    global selectedTeachers
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
    template = loader.get_template('uconnProfViewerApp/search.html')

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

    return HttpResponse(template.render(context,request))