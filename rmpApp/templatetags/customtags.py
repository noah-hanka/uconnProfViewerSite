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
def lower(text):
    return text.lower()
@register.filter
def removePeriods(text):
    return text.replace('.','')