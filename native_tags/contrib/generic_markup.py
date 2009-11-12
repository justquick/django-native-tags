"""
Filters for converting plain text to HTML and enhancing the
typographic appeal of text on the Web.

"""
from django.conf import settings
from django.template import TemplateSyntaxError

from native_tags.decorators import filter
from _markup import formatter

def apply_markup(value, arg=None):
    """
    Applies text-to-HTML conversion.
    
    Takes an optional argument to specify the name of a filter to use.
    
    """
    if arg is not None:
        return formatter(value, filter_name=arg)
    return formatter(value)
apply_markup = filter(apply_markup, is_safe=True)

def smartypants(value):
    """
    Applies SmartyPants to a piece of text, applying typographic
    niceties.
    
    Requires the Python SmartyPants library to be installed; see
    http://web.chad.org/projects/smartypants.py/
    
    """
    try:
        from smartypants import smartyPants
    except ImportError:
        if settings.DEBUG:
            raise TemplateSyntaxError("Error in smartypants filter: the Python smartypants module is not installed or could not be imported")
        return value
    else:
        return smartyPants(value)
smartypants = filter(smartypants, is_safe=True)
