'''
This custom template use inside html for like timestamp, linebreaks tags

'''

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
#from urllib import quote_plus
from django import template

register = template.Library()

@register.filter
def urlify(value):
    return quote(value)
