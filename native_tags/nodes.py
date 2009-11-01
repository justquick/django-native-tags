import re
from shlex import split
from django import template
from django.template import Context, Variable, VariableDoesNotExist
from registry import register


def lookup(var, context, resolve=True):
    """
    Try to resolve the varialbe in a context
    If ``resolve`` is ``False``, only string variables are returned
    """
    if resolve:
        try:
            return Variable(var).resolve(context)
        except VariableDoesNotExist:
            pass
        except TypeError:
            return var
    return unicode(var)

def get_signature(token, contextable=False, comparison=False):
    """
    Gets the signature tuple for any native tag
    contextable searchs for ``as`` variable to update context
    comparison if true uses ``negate`` (p) to ``not`` the result (~p)
    returns (``tag_name``, ``args``, ``kwargs``)
    """
    bits = map(lambda bit: filter(lambda char: char != '\x00', bit), split(token.contents))
    args, kwargs = (), {}
    if comparison and bits[-1] == 'negate':
        bits = bits[:-1]
        kwargs['negate'] = True
    if contextable and len(bits) > 2 and bits[-2] == 'as':
        kwargs['varname'] = bits[-1]
        bits = bits[:-2]
    kwarg_re = re.compile(r'(^[-\w]+)\=(.*)$')
    for bit in bits[1:]:
        match = kwarg_re.match(bit)
        if match:
            kwargs[match.group(1)] = match.group(2)
        else:
            args += (bit,)
    return bits[0], args, kwargs


class NativeNode(template.Node):
    bucket = None
    def __init__(self, name, *args, **kwargs):
        self.func = register[self.bucket][name]
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        resolve = not (hasattr(self.func, 'do_not_resolve') and getattr(self.func, 'do_not_resolve'))
        self.args = (lookup(var, context, resolve) for var in self.args)
        if hasattr(self.func, 'takes_context') and getattr(self.func, 'takes_context'):
            self.args = (context,) + tuple(self.args)
        self.kwargs = dict(((k, lookup(var, context, resolve)) for k, var in self.kwargs.items()))
        return ''

class ComparisonNode(NativeNode):
    bucket = 'comparison'
    def render(self, context):
        super(ComparisonNode, self).render(context)
        nodelist_false = self.kwargs.pop('nodelist_false')
        nodelist_true = self.kwargs.pop('nodelist_true')
        negate = self.kwargs.pop('negate', False)

        try:
            if self.func(*self.args, **self.kwargs):
                if negate:
                    return nodelist_false.render(context)
                return nodelist_true.render(context)
        # If the types don't permit comparison, return nothing.
        except TypeError:
            return ''
        if negate:
            return nodelist_true.render(context)
        return nodelist_false.render(context)


def do_comparison(parser, token):
    """
    Compares two values.

    Syntax::

        {% if_[comparison] [var1] [var2] [var...] [negate] %}
        ...
        {% else %}
        ...
        {% endif_[comparison] %}


    Supported comparisons are ``match``, ``find``, ``startswith``, ``endswith``,
    ``less``, ``less_or_equal``, ``greater`` and ``greater_or_equal`` and many more.
    Checkout the :ref:`contrib-index` for more examples

    Examples::

        {% if_less some_object.id 3 %}
        <p>{{ some_object }} has an id less than 3.</p>
        {% endif_less %}

        {% if_match request.path '^/$' %}
        <p>Welcome home</p>
        {% endif_match %}

    """
    name, args, kwargs = get_signature(token, comparison=True)
    end_tag = 'end' + name
    kwargs['nodelist_true'] = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        kwargs['nodelist_false'] = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        kwargs['nodelist_false'] = template.NodeList()
    return ComparisonNode(name.split('if_')[1], *args, **kwargs)

class FunctionNode(NativeNode):
    bucket = 'function'
    def render(self, context):
        super(FunctionNode, self).render(context)
        varname = self.kwargs.pop('varname', None)
        result = self.func(*self.args, **self.kwargs)
        if hasattr(self.func, 'is_inclusion') and getattr(self.func, 'is_inclusion'):
            template_name, ctx = result
            if not isinstance(ctx, Context):
                ctx = Context(ctx)
            result = get_template(template_name).render(ctx)
        if varname:
            context[varname] = result
            return ''
        return result


def do_function(parser, token):
    """
    Performs a defined function an either outputs results, or stores results in template variable

    Syntax::

        {% [function] [var args...] [name=value kwargs...] [as varname] %}

    Examples::

        {% listdir '.' colors=True as list %}

    """
    name, args, kwargs = get_signature(token, True, True)
    return FunctionNode(name, *args, **kwargs)

class BlockNode(NativeNode):
    bucket = 'block'
    def render(self, context):
        super(BlockNode, self).render(context)
        varname = self.kwargs.pop('varname', None)
        result = self.func(context, self.kwargs.pop('nodelist'), *self.args, **self.kwargs)
        if varname:
            context[varname] = result
            return ''
        return result

def do_block(parser, token):
    """
    Process several nodes inside a single block
    Takes context, nodelist and template arguments

    Syntax::

        {% [block] [var args...] [name=value kwargs...] [as varname] %}
            ... nodelist ...
        {% end[block] %}

    Examples::

        {% count_nodes as nodecount %}
            {{ node1 }}
            ...
        {% endcount_nodes %}

    """
    name, args, kwargs = get_signature(token, contextable=True)
    kwargs['nodelist'] = parser.parse(('end%s' % name,))
    parser.delete_first_token()
    return BlockNode(name, *args, **kwargs)
