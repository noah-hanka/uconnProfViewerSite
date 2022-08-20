import inspect, os.path
import time
import json
import requests

class rmp:
    def __init__(self,uid,filepath = None):
        self.uid = uid
        self.output_file = filepath
        self.teacherDict = self.extractJSON('data/teachers.json')


    #retrieves the HTMl contents of a given url
    def getHTML(self,website):
        try:
            time.sleep(1)
            response = requests.get(website,timeout=None)
        except:
            print("Failed to retrieve HTML content")
            response = None
        return response
    
    #takes json data in the form of a python dictionary and dumps it into a output file in the data/ directory
    def dumpJSON(self,jsondata,filename,folder='data/'):
        if self.output_file == None:
            print("This is running on the web client. No file system active")
            return
        try:
            with open(f'{folder}/{filename}.json','w+') as f:
                json.dump(jsondata,f)
        except:
            print("Failed to save json data")
    
    #extracts from a json file and returns a python dictionary
    def extractJSON(self,filename):
        if self.output_file == None:
            print("This is running on the web client. No file system active")
            return
        try:
            with open(filename, 'r') as f:
                dict = json.load(f)
                return dict
        except:
            return dict()
    
    #searches ratemyprofessors with a query and returns all teachers in the form of json objects
    def search(self,searchQuery):
        #return value of teachers
        teachers = []

        def parseFirstEight():
            #fetches the html from the requested page
            baseurl = 'https://www.ratemyprofessors.com/search/teachers?query='
            searchurl = baseurl+searchQuery+f'&sid={self.uid}'
            htmlContent = self.getHTML(searchurl).text

            #splits html into lines
            lines = htmlContent.splitlines()
            # print(lines)
            #iterates until finds json object or throws error
            i = 0
            while i < len(lines):
                if lines[i][:35] == "          window.__RELAY_STORE__ = ": break
                i += 1
            if i == len(lines): raise Exception("JSON Data could not be found. Possible connection issue...")
            #data is the main json object
            data = lines[i]

            #finds the first teachers data
            teacherStart = data.find('"__typename":"Teacher",')
            #while teachers can be found
            while teacherStart != -1:
                #finds the final teacher attribute

                teacherEnd = data[teacherStart:].find('"isSaved"') + teacherStart + 15
                #appends teacher data to list
                teachers.append(json.loads('{'+data[teacherStart:teacherEnd]+'}'))

                #finds next teacher
                data = data[teacherEnd:]
                teacherStart = data.find('"__typename":"Teacher",')
            #determines if there is a next page and if so, returns the endCursor
            nextPageAttributeIndex = data.find('"hasNextPage"')+14
            hasNextPage = data[nextPageAttributeIndex:nextPageAttributeIndex+4]
            if hasNextPage == 'true':
                hasNextPage = True
                endCursorStart = data.find('"endCursor"')+13
                endCursorEnd = data[endCursorStart:].find('}')+endCursorStart-1
                endCursor = data[endCursorStart:endCursorEnd]
            else:
                hasNextPage = False
                endCursor = None
            return (hasNextPage, endCursor)
        def fetchOtherTeachers(endCursor):
            cookies = {
                '_gid': 'GA1.2.547176395.1660854978',
                '_scid': 'f0e5bc82-f75c-4a65-b86c-13c2b42240f5',
                '_pbjs_userid_consent_data': '3524755945110770',
                '_pubcid': '97689d16-9207-4401-b2a4-d3a29e0b8194',
                'ccpa-notice-viewed-02': 'true',
                'trc_cookie_storage': 'taboola%2520global%253Auser-id%3D130a1ff3-c330-431b-8ec2-c9fc52a2330a-tuct826e943',
                'panoramaId_expiry': '1661459785504',
                '_cc_id': 'c804416de7d496cdcf87375dd2034c5d',
                'panoramaId': '3362d8c6c15235a17e56777ff68616d539385f1e1a90dd61465c07fed24d7bcc',
                'pjs-unifiedid': '%7B%22TDID%22%3A%226f3c050a-844c-4282-8355-cb3d65fba175%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222022-07-18T20%3A19%3A57%22%7D',
                '_li_dcdm_c': '.ratemyprofessors.com',
                '_lc2_fpi': '5ee24c8f6482--01gasaqy64rgzzb7xm8y4v7hna',
                '_sctr': '1|1660795200000',
                '_lr_env_src_ats': 'false',
                'pbjs-unifiedid': '%7B%22TDID%22%3A%226f3c050a-844c-4282-8355-cb3d65fba175%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222022-07-18T20%3A19%3A57%22%7D',
                'pbjs_li_nonid': '%7B%7D',
                '__qca': 'I0-1468004258-1660855835274',
                '_hjSessionUser_1667000': 'eyJpZCI6Ijk1OTdjMjBkLWNiOGEtNWI5OS05OGVmLWZkMjcxODVhMGJiNyIsImNyZWF0ZWQiOjE2NjA4NTQ5Nzc5NzQsImV4aXN0aW5nIjp0cnVlfQ==',
                '_hjAbsoluteSessionInProgress': '0',
                '_hjIncludedInSessionSample': '0',
                '_hjSession_1667000': 'eyJpZCI6ImU4NWQzZDVhLTcxYzMtNDc3Yy05NDI0LTViYmU0ZWMyZmM2ZiIsImNyZWF0ZWQiOjE2NjA4Njc1MTQwNjcsImluU2FtcGxlIjpmYWxzZX0=',
                'bounceClientVisit3905v': 'N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0ATgIYICmAtgJ4QUD2AZrSiqxSmQGNW9IilpUKAuETpUptPpnwBHAK4LGmACJU8ANhQBLACbaAqrgByrAEa4AnCgAyAFQCKADwDyLs9pAANCAUMCCBIIYoAPoA5qxRYtyGrAB2MOxUYGJBkbEQCVxGqemZYgC+QA',
                '_lr_retry_request': 'true',
                'userSchoolId': 'U2Nob29sLTEwOTE=',
                'userSchoolLegacyId': '1091',
                'userSchoolName': 'University%20of%20Connecticut',
                '_ga_WET17VWCJ3': 'GS1.1.1660867499.4.1.1660869810.0.0.0',
                '_ga': 'GA1.1.497815230.1660854978',
                'cto_bidid': 'brNLEV9xTlNvZkdmTGVkcUVGQ2ZJTnFrOXE3VnVLT0k4TFFVdkhKSWVFdzgxUnhvYkowMWtmMDliUldnTjd1WHozQTN4UE9xV0ZsdHNLMVZjaG41dFhVMDVFZnRkZ0RsUHZiTEEwaWJ6RjFLRHkwT0hFdzhYdlRIaEl5dVQlMkJxakhTWURZ',
                'cto_bundle': 'jy87wV9GdkRxdEQzcDdieG5UdFpqYjBBdUFDR3dGSHZ3SEpXSXIxdVoxN0JSOU15JTJCVE9KTXFNdm5nNjM1VWVWRWRzMHZmUlNSalk4emttRGZVa0lqc1BCWElPMmFqUGZJdnZOVGF0c1NrT0dXWnZsVnZ0cDJLM0NIdGFRYiUyRnppR04xSFlNUFE2dVMzUGNvUDFsbDRhcjdFWFY0ODFlZUJ6c2QzZ0VabnB5ZHVBZE4wJTNE',
                'cto_bundle': '9wi7nF9GdkRxdEQzcDdieG5UdFpqYjBBdUFOeHBuUHFGdDBFTHBNQWt3aTJIalJqME96dndqbWdINm8xRjVZdjZqdG5RaSUyQnF6JTJGVWF2OGRWNjVzQ0YlMkJBU2lBV0QlMkI2ellkUWtDcXJocWttbExOUnElMkJOZ0J3Z0c5MHl3YUpQVDlXNmJoRm1WQiUyQjhsdE5HJTJCeXNFZ0I0RjFjdnZQcnVKemlzSFp2JTJGZlhwb1RNYWR3SW93JTNE',
                'cto_bundle': '9wi7nF9GdkRxdEQzcDdieG5UdFpqYjBBdUFOeHBuUHFGdDBFTHBNQWt3aTJIalJqME96dndqbWdINm8xRjVZdjZqdG5RaSUyQnF6JTJGVWF2OGRWNjVzQ0YlMkJBU2lBV0QlMkI2ellkUWtDcXJocWttbExOUnElMkJOZ0J3Z0c5MHl3YUpQVDlXNmJoRm1WQiUyQjhsdE5HJTJCeXNFZ0I0RjFjdnZQcnVKemlzSFp2JTJGZlhwb1RNYWR3SW93JTNE',
            }

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Authorization': 'Basic dGVzdDp0ZXN0',
                'Connection': 'keep-alive',
                'Origin': 'https://www.ratemyprofessors.com',
                'Referer': 'https://www.ratemyprofessors.com/search/teachers?query=a&sid=U2Nob29sLTEwOTE=',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            json_data = {
                'query': 'query TeacherSearchPaginationQuery(\n  $count: Int!\n  $cursor: String\n  $query: TeacherSearchQuery!\n) {\n  search: newSearch {\n    ...TeacherSearchPagination_search_1jWD3d\n  }\n}\n\nfragment TeacherSearchPagination_search_1jWD3d on newSearch {\n  teachers(query: $query, first: $count, after: $cursor) {\n    didFallback\n    edges {\n      cursor\n      node {\n        ...TeacherCard_teacher\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n    resultCount\n    filters {\n      field\n      options {\n        value\n        id\n      }\n    }\n  }\n}\n\nfragment TeacherCard_teacher on Teacher {\n  id\n  legacyId\n  avgRating\n  numRatings\n  ...CardFeedback_teacher\n  ...CardSchool_teacher\n  ...CardName_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment CardFeedback_teacher on Teacher {\n  wouldTakeAgainPercent\n  avgDifficulty\n}\n\nfragment CardSchool_teacher on Teacher {\n  department\n  school {\n    name\n    id\n  }\n}\n\nfragment CardName_teacher on Teacher {\n  firstName\n  lastName\n}\n\nfragment TeacherBookmark_teacher on Teacher {\n  id\n  isSaved\n}\n',
                'variables': {
                    'count': 1000,
                    'cursor': endCursor,
                    'query': {
                        'text': f'{searchQuery}',
                        'schoolID': self.uid,
                        'fallback': False,
                        'departmentID': None,
                    },
                },
            }

            response = requests.post('https://www.ratemyprofessors.com/graphql', cookies=cookies, headers=headers, json=json_data)
            teacherList = response.json()['data']['search']['teachers']['edges']
            for teacher in teacherList:
                teachers.append(teacher['node'])
        hasNextPage, endCursor = parseFirstEight()
        if hasNextPage:
            fetchOtherTeachers(endCursor)
        
        teacherDict = dict()
        for teacher in teachers:
            firstname = teacher['firstName']
            lastname = teacher['lastName']
            legacyId = teacher['legacyId']
            teacherDict[f'{firstname}_{lastname}_{legacyId}'] = teacher

        return teacherDict

    #reinitializes self.teachersDict and updates it with all current teachers 
    def searchAllProf(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        baseurl = 'https://www.ratemyprofessors.com/search/teachers?query='
        self.teacherDict = dict()
        for c in alphabet:
            teachers = self.searchRMP(c)
            for teacher in teachers:
                firstname = teacher['firstName']
                lastname = teacher['lastName']
                legacyId = teacher['legacyId']
                self.teacherDict[f'{firstname}_{lastname}_{legacyId}'] = teacher
            print(f"All teachers containing {c} in their name added to dictionary.")

    #retrieves the data of a specified professor given their id
    def fetchProfData(self,legacyId,tid):
        metrics = {'professor':dict(),'distribution':dict(),'reviews':[]}
        #gets the indepth data about the professor, and the initial reviews about the professor
        def getMetricsAndInitialReviews():
            profURL = f"https://www.ratemyprofessors.com/ShowRatings.jsp?tid={legacyId}"
            htmlContent = self.getHTML(profURL).text

            #splits html into lines
            lines = htmlContent.splitlines()
            #iterates until finds json object or throws error
            i = 0
            while i < len(lines):
                if lines[i][:35] == "          window.__RELAY_STORE__ = ": break
                i += 1
            if i == len(lines): raise Exception("JSON Data could not be found. Possible connection issue...")
            #data is the main json object
            data = lines[i]
            
            #get the teacher stats and add it to metrics
            teacherStart = data.find('"__typename":"Teacher"')+23
            teacherEnd = data[teacherStart:].find(',"relatedTeachers"')+teacherStart
            stats_string = '{'+data[teacherStart:teacherEnd]+'}'
            stats = json.loads(stats_string)
            if 'school' in stats: stats.pop('school')
            if 'ratingsDistribution' in stats: stats.pop('ratingsDistribution')
            if 'teacherRatingTags' in stats: stats.pop('teacherRatingTags')
            metrics['professor'] = stats

            #this means page does not exists
            if metrics['professor'] == {}: return (None, None)

            #gets rating distributions and adds it to metrics
            data = data[teacherEnd+1:]
            distributionStart = data.find('"__typename":"ratingsDistribution",')+35
            distributionEnd = data[distributionStart:].find('}')+distributionStart
            jsonDistribution = json.loads('{'+data[distributionStart:distributionEnd]+'}')
            metrics['distribution'] = jsonDistribution

            data = data[distributionEnd+1:]
            
            ratingStart = data.find('"__typename":"Rating"')+22
            while ratingStart>=22:
                ratingEnd = data[ratingStart:].find('thumbs"')-2+ratingStart
                metrics['reviews'].append(json.loads('{'+data[ratingStart:ratingEnd]+'}'))
                data = data[ratingEnd:]
                ratingStart = data.find('"__typename":"Rating"')+22

            #determines if there is a next page and if so, returns the endCursor
            nextPageAttributeIndex = data.find('"hasNextPage"')+14
            hasNextPage = data[nextPageAttributeIndex:nextPageAttributeIndex+4]
            if hasNextPage == 'true':
                hasNextPage = True
                endCursorStart = data.find('"endCursor"')+13
                endCursorEnd = data[endCursorStart:].find('}')+endCursorStart-1
                endCursor = data[endCursorStart:endCursorEnd]
                print(endCursor)
            else:
                hasNextPage = False
                endCursor = None
            return (hasNextPage, endCursor)
        def fetchOtherReviews(endCursor):
            #necessary tags for post request
            cookies = {
                '_gid': 'GA1.2.547176395.1660854978',
                '_scid': 'f0e5bc82-f75c-4a65-b86c-13c2b42240f5',
                '_pbjs_userid_consent_data': '3524755945110770',
                '_pubcid': '97689d16-9207-4401-b2a4-d3a29e0b8194',
                'ccpa-notice-viewed-02': 'true',
                'trc_cookie_storage': 'taboola%2520global%253Auser-id%3D130a1ff3-c330-431b-8ec2-c9fc52a2330a-tuct826e943',
                'panoramaId_expiry': '1661459785504',
                '_cc_id': 'c804416de7d496cdcf87375dd2034c5d',
                'panoramaId': '3362d8c6c15235a17e56777ff68616d539385f1e1a90dd61465c07fed24d7bcc',
                'pjs-unifiedid': '%7B%22TDID%22%3A%226f3c050a-844c-4282-8355-cb3d65fba175%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222022-07-18T20%3A19%3A57%22%7D',
                '_li_dcdm_c': '.ratemyprofessors.com',
                '_lc2_fpi': '5ee24c8f6482--01gasaqy64rgzzb7xm8y4v7hna',
                '_sctr': '1|1660795200000',
                '_lr_env_src_ats': 'false',
                'pbjs-unifiedid': '%7B%22TDID%22%3A%226f3c050a-844c-4282-8355-cb3d65fba175%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222022-07-18T20%3A19%3A57%22%7D',
                'pbjs_li_nonid': '%7B%7D',
                '__qca': 'I0-1468004258-1660855835274',
                '_hjSessionUser_1667000': 'eyJpZCI6Ijk1OTdjMjBkLWNiOGEtNWI5OS05OGVmLWZkMjcxODVhMGJiNyIsImNyZWF0ZWQiOjE2NjA4NTQ5Nzc5NzQsImV4aXN0aW5nIjp0cnVlfQ==',
                'userSchoolId': 'U2Nob29sLTEwOTE=',
                'userSchoolLegacyId': '1091',
                'userSchoolName': 'University%20of%20Connecticut',
                '_gat': '1',
                '_ga_WET17VWCJ3': 'GS1.1.1660882356.6.1.1660882358.0.0.0',
                '_ga': 'GA1.1.497815230.1660854978',
                'cto_bidid': 'y2CzmV9xTlNvZkdmTGVkcUVGQ2ZJTnFrOXE3VnVLT0k4TFFVdkhKSWVFdzgxUnhvYkowMWtmMDliUldnTjd1WHozQTN4UE9xV0ZsdHNLMVZjaG41dFhVMDVFZnRkZ0RsUHZiTEEwaWJ6RjFLRHkwTUlpbGNPRFNGOU1lR1ltVXlnWXhkNA',
                'cto_bundle': 'PADiLl9GdkRxdEQzcDdieG5UdFpqYjBBdUFDZkJoSExtUno3U0xQNzYxd3hZTEVNd09SJTJGalJhb3E5V3FOeWU1UmJlVXZsUzNXeVhXRUxSNk84NWdwTmkxUG5NWXRQQVBXUlhSVE0lMkZ5MGJTNVdEZ0haaFVMb2JYNTZITVB6WkcwWUQ1NjhNdUFBdSUyQmNuUGV3ZXowMENMSzR2YjVEaVhDRk1mVnVRQ2Vpb3gwM0RRQTglM0Q',
                '_hjIncludedInSessionSample': '0',
                '_hjSession_1667000': 'eyJpZCI6ImE5NTVlMGQ4LTA3NDAtNDE5Yi1hNjc0LTRiNTdhNDFkMmYzYyIsImNyZWF0ZWQiOjE2NjA4ODIzNTkxMjksImluU2FtcGxlIjpmYWxzZX0=',
                '_hjAbsoluteSessionInProgress': '0',
                'bounceClientVisit3905v': 'N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0ATgIYICmAtgJ4QUD2AZrSiqxSmQGNW9IgGU4rYgCUaASwB2Ac34ArFBEz4EsgCaYAIrgCsxgIwYMIADQgKMENZCyUAfUWsXKLilmt5MdiowLxtnNwhPb19-aEDg2gBfIA',
                '_lr_retry_request': 'true',
                'cto_bundle': '4kJiW19GdkRxdEQzcDdieG5UdFpqYjBBdUFPcXJGMURxTFFLVGQlMkZCZWdRa3UyN3BXR0xQJTJGMFA0Rk00U3BuYXdab2VyNldCNDZsaUNjZm9TbGpSWjZWNDRpOFIybWhYZGpHRVJjSkZLY2ZCYkl5RUo0YiUyRldyODhWRTdxektQeTVoVzNNbzdzY3h3bjQwNXBYSW5ZRTlWUGliMk9nRjU1Vk4zbHpNVDVtejhhT0FhcWMlM0Q',
                'cto_bundle': '4kJiW19GdkRxdEQzcDdieG5UdFpqYjBBdUFPcXJGMURxTFFLVGQlMkZCZWdRa3UyN3BXR0xQJTJGMFA0Rk00U3BuYXdab2VyNldCNDZsaUNjZm9TbGpSWjZWNDRpOFIybWhYZGpHRVJjSkZLY2ZCYkl5RUo0YiUyRldyODhWRTdxektQeTVoVzNNbzdzY3h3bjQwNXBYSW5ZRTlWUGliMk9nRjU1Vk4zbHpNVDVtejhhT0FhcWMlM0Q',
            }

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Authorization': 'Basic dGVzdDp0ZXN0',
                'Connection': 'keep-alive',
                'Origin': 'https://www.ratemyprofessors.com',
                'Referer': f'https://www.ratemyprofessors.com/ShowRatings.jsp?tid={legacyId}',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            json_data = {
                'query': 'query RatingsListQuery(\n  $count: Int!\n  $id: ID!\n  $courseFilter: String\n  $cursor: String\n) {\n  node(id: $id) {\n    __typename\n    ... on Teacher {\n      ...RatingsList_teacher_4pguUW\n    }\n    id\n  }\n}\n\nfragment RatingsList_teacher_4pguUW on Teacher {\n  id\n  legacyId\n  lastName\n  numRatings\n  school {\n    id\n    legacyId\n    name\n    city\n    state\n    avgRating\n    numRatings\n  }\n  ...Rating_teacher\n  ...NoRatingsArea_teacher\n  ratings(first: $count, after: $cursor, courseFilter: $courseFilter) {\n    edges {\n      cursor\n      node {\n        ...Rating_rating\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n  }\n}\n\nfragment Rating_teacher on Teacher {\n  ...RatingFooter_teacher\n  ...RatingSuperHeader_teacher\n  ...ProfessorNoteSection_teacher\n}\n\nfragment NoRatingsArea_teacher on Teacher {\n  lastName\n  ...RateTeacherLink_teacher\n}\n\nfragment Rating_rating on Rating {\n  comment\n  flagStatus\n  createdByUser\n  teacherNote {\n    id\n  }\n  ...RatingHeader_rating\n  ...RatingSuperHeader_rating\n  ...RatingValues_rating\n  ...CourseMeta_rating\n  ...RatingTags_rating\n  ...RatingFooter_rating\n  ...ProfessorNoteSection_rating\n}\n\nfragment RatingHeader_rating on Rating {\n  date\n  class\n  helpfulRating\n  clarityRating\n  isForOnlineClass\n}\n\nfragment RatingSuperHeader_rating on Rating {\n  legacyId\n}\n\nfragment RatingValues_rating on Rating {\n  helpfulRating\n  clarityRating\n  difficultyRating\n}\n\nfragment CourseMeta_rating on Rating {\n  attendanceMandatory\n  wouldTakeAgain\n  grade\n  textbookUse\n  isForOnlineClass\n  isForCredit\n}\n\nfragment RatingTags_rating on Rating {\n  ratingTags\n}\n\nfragment RatingFooter_rating on Rating {\n  id\n  comment\n  adminReviewedAt\n  flagStatus\n  legacyId\n  thumbsUpTotal\n  thumbsDownTotal\n  thumbs {\n    userId\n    thumbsUp\n    thumbsDown\n    id\n  }\n  teacherNote {\n    id\n  }\n}\n\nfragment ProfessorNoteSection_rating on Rating {\n  teacherNote {\n    ...ProfessorNote_note\n    id\n  }\n  ...ProfessorNoteEditor_rating\n}\n\nfragment ProfessorNote_note on TeacherNotes {\n  comment\n  ...ProfessorNoteHeader_note\n  ...ProfessorNoteFooter_note\n}\n\nfragment ProfessorNoteEditor_rating on Rating {\n  id\n  legacyId\n  class\n  teacherNote {\n    id\n    teacherId\n    comment\n  }\n}\n\nfragment ProfessorNoteHeader_note on TeacherNotes {\n  createdAt\n  updatedAt\n}\n\nfragment ProfessorNoteFooter_note on TeacherNotes {\n  legacyId\n  flagStatus\n}\n\nfragment RateTeacherLink_teacher on Teacher {\n  legacyId\n  numRatings\n  lockStatus\n}\n\nfragment RatingFooter_teacher on Teacher {\n  id\n  legacyId\n  lockStatus\n  isProfCurrentUser\n}\n\nfragment RatingSuperHeader_teacher on Teacher {\n  firstName\n  lastName\n  legacyId\n  school {\n    name\n    id\n  }\n}\n\nfragment ProfessorNoteSection_teacher on Teacher {\n  ...ProfessorNote_teacher\n  ...ProfessorNoteEditor_teacher\n}\n\nfragment ProfessorNote_teacher on Teacher {\n  ...ProfessorNoteHeader_teacher\n  ...ProfessorNoteFooter_teacher\n}\n\nfragment ProfessorNoteEditor_teacher on Teacher {\n  id\n}\n\nfragment ProfessorNoteHeader_teacher on Teacher {\n  lastName\n}\n\nfragment ProfessorNoteFooter_teacher on Teacher {\n  legacyId\n  isProfCurrentUser\n}\n',
                'variables': {
                    'count': 100,
                    'id': tid,
                    'courseFilter': None,
                    'cursor': endCursor,
                },
            }
            response = requests.post('https://www.ratemyprofessors.com/graphql', cookies=cookies, headers=headers, json=json_data)
            reviewList = response.json()['data']['node']["ratings"]["edges"]
            #pulls post request, removes extra keys,and adds to dictionary list
            for review in reviewList:
                reviewdata = review["node"]
                reviewdata.pop("__typename")
                reviewdata.pop("thumbs")
                metrics['reviews'].append(reviewdata)
            return
        
        hasNextPage, endCursor = getMetricsAndInitialReviews()
        
        #if page doesn't exist, return empty json data
        if metrics['professor'] == {}:
            print(f"Page does not exist for {tid}")
            return metrics
        #if there are additional reviews not laoded, fetch them, passing in the last cursor
        if hasNextPage:
            fetchOtherReviews(endCursor)
        return metrics
    
    #saves a professors data given their dictionary into a json file
    def saveProfData(self,data):
        if self.output_file == None:
            print("This is running on the web client. No file system active")
            return
        professorDict = data['professor']

        #no data to save
        if professorDict == {}:
            return

        #get the stuff to name the file and dump it
        firstName = professorDict['firstName']
        lastName = professorDict['lastName']
        legacyId = professorDict['legacyId']
        filename = f'{firstName}_{lastName}_{legacyId}'
        self.dumpJSON(data,filename,folder='data/professors/')
        print(f'{filename} was saved successfully.')
        return
    
    #saves all professors in self.teachersdict
    def saveAllProfessors(self):
        if self.output_file == None:
            print("This is running on the web client. No file system active")
            return
        for professor in self.teacherDict.values():
            data = self.getProfData(professor)
            self.saveProfData(data)
        return

if __name__ == "__main__":
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    cwd     = os.path.dirname(os.path.abspath(filename))
    output_file = cwd+'/output.txt'
    uconn_id = 'U2Nob29sLTEwOTE='
    uconn_rmp = rmp(uconn_id)
    jakeresults = uconn_rmp.search('anaiscniwnanw')
    print(jakeresults)