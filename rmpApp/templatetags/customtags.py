from django import template

register = template.Library()

@register.filter
def dic(dic,key):
    return dic[key]
@register.filter
def na(value):
    return "N/A" if value == -1 else value