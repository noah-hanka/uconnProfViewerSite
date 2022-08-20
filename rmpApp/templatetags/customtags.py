from contextlib import redirect_stderr
from django import template

register = template.Library()

@register.filter
def dic(dic,key):
    return dic[key]
@register.filter
def na(value):
    return "N/A" if value == -1 else str(value)+'%'
@register.filter
def ratingcolor(value):
    value = int(value)
    color = '#FF6961'
    if value >= 2.5:
        color = '#F8D66D'
    if value >= 4:
        color = '#8CD47E'
    return color