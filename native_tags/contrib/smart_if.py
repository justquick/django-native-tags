from django.template import TemplateSyntaxError
from native_tags.decorators import comparison

OPERATORS = {
    '=': lambda x, y: x == y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    '<': lambda x, y: x < y,
    'or': lambda x, y: x or y,
    'and': lambda x, y: x and y,
    'in': lambda x, y: x in y,
}

def semi_smart_if(var1, operator=None, var2=None):
    '''
    Idea adapted from this djangosnippet: http://www.djangosnippets.org/snippets/1350/
    
    WARNING: This is not a functional replacement to the above solution as it currently lacks
    the capability of multiple operations like
    
        {% if a > b and a < b %}
    
    A smarter {% if %} tag for django templates.

    While retaining current Django functionality, it also handles equality,
    greater than and less than operators. Some common case examples::

        {% if articles|length >= 5 %}...{% endif %}
        {% if "ifnotequal tag" != "beautiful" %}...{% endif %}

    Arguments and operators _must_ have a space between them, so
    ``{% if 1>2 %}`` is not a valid smart if tag.

    All supported operators are: ``or``, ``and``, ``in``, ``=`` (or ``==``),
    ``!=``, ``>``, ``>=``, ``<`` and ``<=``.
    '''
    if operator is None and var2 is None:
        # {% if user.is_authenticated %}
        return var1
    if not operator in OPERATORS:
        raise TemplateSyntaxError('%r is not a valid operator.' % operator)
    return OPERATORS[operator](var1, var2)
semi_smart_if = comparison(semi_smart_if, name='if')
