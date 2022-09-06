from contextlib import redirect_stderr
from django import template

register = template.Library()

@register.filter
def dic(dic,key):
    return dic[key]
@register.filter
def na(value):
    return "n/a" if value == -1 else str(value)+'%'
@register.filter
def ratingcolor(value):
    value = int(value)
    color = '#7C878E'
    if value > 0:
        color = '#FF6961'
    if value >= 2.5:
        color = '#F8D66D'
    if value >= 4:
        color = '#8CD47E'
    return color
@register.filter
def difficultycolor(value):
    value = int(value)
    color = '#7C878E'
    if value > 0:
        color = '#8CD47E'
    if value >= 3.0:
        color = '#F8D66D'
    if value >= 4:
        color = '#FF6961'
    return color
@register.filter
def lower(text):
    return text.lower()
@register.filter
def removePeriods(text):
    return text.replace('.','')
@register.filter
def emptySearch(text):
    return text if text.strip() != '' else 'uconn'
@register.filter
def getRating(review):
    clarity = review['clarityRating']
    helpful = review['helpfulRating']
    return str((clarity+helpful)//2)
@register.filter
def convertDate(datestring):
    #2022-05-09 04:04:15 +0000 UTC
    datestring = datestring.split(' ')[0].split('-')
    year = datestring[0]
    month  = datestring[1]
    day = datestring[2]

    months = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
    month = months[month]

    if day[0] == '0': day = day[1]

    return f'{month} {day}, {year}'
@register.filter
def textbookConvert(textbookUse):
    if textbookUse == 5:
        return 'yes'
    elif textbookUse == 0:
        return 'no'
    else:
        return 'n/a'
@register.filter
def gradeNA(grade):
    return 'N/A' if grade == '' else grade
@register.filter
def wouldTakeAgainConvert(wouldTakeAgain):
    return 'yes' if wouldTakeAgain == 1 else 'no'