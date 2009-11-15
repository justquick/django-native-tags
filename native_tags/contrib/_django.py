"""Default tags used by the template system, available to all templates."""

import sys
import re
from itertools import cycle as itertools_cycle
try:
    reversed
except NameError:
    from django.utils.itercompat import reversed     # Python 2.3 fallback

from django.template import Node, NodeList, Template, Context, Variable
from django.template import TemplateSyntaxError, VariableDoesNotExist, BLOCK_TAG_START, BLOCK_TAG_END, VARIABLE_TAG_START, VARIABLE_TAG_END, SINGLE_BRACE_START, SINGLE_BRACE_END, COMMENT_TAG_START, COMMENT_TAG_END
from django.template import get_library, Library, InvalidTemplateLibrary
from django.conf import settings
from django.utils.encoding import smart_str, smart_unicode
from django.utils.itercompat import groupby
from django.utils.safestring import mark_safe

def autoescape(context, nodelist, setting):
    """
    Force autoescape behaviour for this block.
    """
    old_setting = context.autoescape
    context.autoescape = setting
    output = nodelist.render(context)
    context.autoescape = old_setting
    if setting:
        return mark_safe(output)
    else:
        return output
autoescape.block = 1

def comment(context, nodelist):
    """
    Ignores everything between ``{% comment %}`` and ``{% endcomment %}``.
    """
    return ''
comment.block = 1

def cycle(context, *cyclevars):
    """
    Cycles among the given strings each time this tag is encountered.

    Within a loop, cycles among the given strings each time through
    the loop::

        {% for o in some_list %}
            <tr class="{% cycle 'row1' 'row2' %}">
                ...
            </tr>
        {% endfor %}

    Outside of a loop, give the values a unique name the first time you call
    it, then use that name each sucessive time through::

            <tr class="{% cycle 'row1' 'row2' 'row3' as rowcolors %}">...</tr>
            <tr class="{% cycle rowcolors %}">...</tr>
            <tr class="{% cycle rowcolors %}">...</tr>

    You can use any number of values, separated by spaces. Commas can also
    be used to separate values; if a comma is used, the cycle values are
    interpreted as literal strings.
    """

    return itertools_cycle(cyclevars).next()
cycle.function = 1

def debug(context):
    """
    Outputs a whole load of debugging information, including the current
    context and imported modules.

    Sample usage::

        <pre>
            {% debug %}
        </pre>
    """

    from pprint import pformat
    output = [pformat(val) for val in context]
    output.append('\n\n')
    output.append(pformat(sys.modules))
    return ''.join(output)
debug.function = 1

def filter(context, nodelist, filter_exp):
    """
    Filters the contents of the block through variable filters.

    Filters can also be piped through each other, and they can have
    arguments -- just like in variable syntax.

    Sample usage::

        {% filter force_escape|lower %}
            This text will be HTML-escaped, and will appear in lowercase.
        {% endfilter %}
    """
    output = nodelist.render(context)
    # Apply filters.
    context.update({'var': output})
    filtered = filter_expr.resolve(context)
    context.pop()
    return filtered
filter.block = 1

def firstof(*vars):
    """
    Outputs the first variable passed that is not False, without escaping.

    Outputs nothing if all the passed variables are False.

    Sample usage::

        {% firstof var1 var2 var3 %}

    This is equivalent to::

        {% if var1 %}
            {{ var1|safe }}
        {% else %}{% if var2 %}
            {{ var2|safe }}
        {% else %}{% if var3 %}
            {{ var3|safe }}
        {% endif %}{% endif %}{% endif %}

    but obviously much cleaner!

    You can also use a literal string as a fallback value in case all
    passed variables are False::

        {% firstof var1 var2 var3 "fallback value" %}

    If you want to escape the output, use a filter tag::

        {% filter force_escape %}
            {% firstof var1 var2 var3 "fallback value" %}
        {% endfilter %}

    """
    for var in vars:
        if var:
            return var
firstof.function = 1

def regroup(target, expression):
    """
    Regroups a list of alike objects by a common attribute.

    This complex tag is best illustrated by use of an example:  say that
    ``people`` is a list of ``Person`` objects that have ``first_name``,
    ``last_name``, and ``gender`` attributes, and you'd like to display a list
    that looks like:

        * Male:
            * George Bush
            * Bill Clinton
        * Female:
            * Margaret Thatcher
            * Colendeeza Rice
        * Unknown:
            * Pat Smith

    The following snippet of template code would accomplish this dubious task::

        {% regroup people by gender as grouped %}
        <ul>
        {% for group in grouped %}
            <li>{{ group.grouper }}
            <ul>
                {% for item in group.list %}
                <li>{{ item }}</li>
                {% endfor %}
            </ul>
        {% endfor %}
        </ul>

    As you can see, ``{% regroup %}`` populates a variable with a list of
    objects with ``grouper`` and ``list`` attributes.  ``grouper`` contains the
    item that was grouped by; ``list`` contains the list of objects that share
    that ``grouper``.  In this case, ``grouper`` would be ``Male``, ``Female``
    and ``Unknown``, and ``list`` is the list of people with those genders.

    Note that ``{% regroup %}`` does not work when the list to be grouped is not
    sorted by the key you are grouping by!  This means that if your list of
    people was not sorted by gender, you'd need to make sure it is sorted
    before using it, i.e.::

        {% regroup people|dictsort:"gender" by gender as grouped %}

    """
    if not target: return ''
    return [
        # List of dictionaries in the format:
        # {'grouper': 'key', 'list': [list of contents]}.
        {'grouper': key, 'list': list(val)}
        for key, val in
        groupby(obj_list, lambda v, f=expression.resolve: f(v, True))
    ]
regroup.function = 1

def now(format_string):
    """
    Displays the date, formatted according to the given string.

    Uses the same format as PHP's ``date()`` function; see http://php.net/date
    for all the possible values.

    Sample usage::

        It is {% now "jS F Y H:i" %}
    """
    from datetime import datetime
    from django.utils.dateformat import DateFormat
    return DateFormat(datetime.now()).format(self.format_string)
now.function = 1

def spaceless(context, nodelists):
    """
    Removes whitespace between HTML tags, including tab and newline characters.

    Example usage::

        {% spaceless %}
            <p>
                <a href="foo/">Foo</a>
            </p>
        {% endspaceless %}

    This example would return this HTML::

        <p><a href="foo/">Foo</a></p>

    Only space between *tags* is normalized -- not space between tags and text.
    In this example, the space around ``Hello`` won't be stripped::

        {% spaceless %}
            <strong>
                Hello
            </strong>
        {% endspaceless %}
    """

    from django.utils.html import strip_spaces_between_tags
    return strip_spaces_between_tags(nodelist.render(context).strip())
spaceless.block = 1

def widthratio(value, maxvalue, max_width):
    """
    For creating bar charts and such, this tag calculates the ratio of a given
    value to a maximum value, and then applies that ratio to a constant.

    For example::

        <img src='bar.gif' height='10' width='{% widthratio this_value max_value 100 %}' />

    Above, if ``this_value`` is 175 and ``max_value`` is 200, the image in
    the above example will be 88 pixels wide (because 175/200 = .875;
    .875 * 100 = 87.5 which is rounded up to 88).
    """
    try:
        max_width = int(max_width)
    except ValueError:
        raise TemplateSyntaxError("widthratio final argument must be an number")
    try:
        value = float(value)
        maxvalue = float(maxvalue)
        ratio = (value / maxvalue) * max_width
    except (ValueError, ZeroDivisionError):
        return ''
    return str(int(round(ratio)))
widthratio.function = 1

def with_(context, nodelist, val):
    """
    Adds a value to the context (inside of this block) for caching and easy
    access.

    For example::

        {% with person.some_sql_method as total %}
            {{ total }} object{{ total|pluralize }}
        {% endwith %}
    """
    context.push()
    context[self.name] = val
    output = nodelist.render(context)
    context.pop()
    return output
with_.block = 1
