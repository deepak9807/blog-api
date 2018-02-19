'''
This custom template use inside html for like timestamp, linebreaks tags

'''
from urllib import quote_plus
from django import template

register = template.Library()

@register.filter
def urlify(value):
    return quote_plus(value)
