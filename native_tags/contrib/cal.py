from calendar import HTMLCalendar
from native_tags.decorators import function

def calendar(format, *args, **kwargs):
    """
    Creates a formatted ``HTMLCalendar``. 
    Argument ``format`` can be one of ``month``, ``year``, or ``yearpage``
    Keyword arguments are collected and passed into ``HTMLCalendar.formatmonth``, 
    ``HTMLCalendar.formatyear``, and ``HTMLCalendar.formatyearpage``
    
        Syntax::
            
            {% calendar month [year] [month] %}
            {% calendar year [year] %}
            {% calendar yearpage [year] %}
            
        Example::
        
            {% calendr month 2009 10 %}
    """
    cal = HTMLCalendar(kwargs.pop('firstweekday', 0))
    return getattr(cal, 'format%s' % format)(*args, **kwargs)
calendar = function(calendar)

