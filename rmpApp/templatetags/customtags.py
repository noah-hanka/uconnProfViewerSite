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
