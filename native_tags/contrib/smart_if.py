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

def smart_if(var1, operator, var2):
    '''
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
    if not operator in OPERATORS:
        raise TemplateSyntaxError('%r is not a valid operator.' % operator)
    return OPERATORS[operator](var1, var2)
smart_if = comparison(smart_if, name='if')
