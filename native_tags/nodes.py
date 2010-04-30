import re
from shlex import split
from django import template
from django.template import Context, Variable, VariableDoesNotExist
from django.template.loader import get_template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.hashcompat import sha_constructor
from django.core.cache import cache
from registry import register
from settings import DEFAULT_CACHE_TIMEOUT

class Constant(unicode):
    """Just a placeholder unicode constant so you can tell
    which variables failed lookup and should be considered constant.
    You can tell by using ``isinstance(var_or_constant, Constant)``"""
    pass

def lookup(parser, var, context, resolve=True, apply_filters=True):
    """
    Try to resolve the varialbe in a context
    If ``resolve`` is ``False``, only string variables are returned
    """
    if resolve:
        try:
            return Variable(var).resolve(context)
        except VariableDoesNotExist:
            if apply_filters and var.find('|') > -1:
                return parser.compile_filter(var).resolve(context)
            return Constant(var)
        except TypeError:
            # already resolved
            return var
    return var

def get_cache_key(bucket, name, args, kwargs):
    """
    Gets a unique SHA1 cache key for any call to a native tag.
    Use args and kwargs in hash so that the same arguments use the same key
    """
    u = ''.join(map(str, (bucket, name, args, kwargs)))
    return 'native_tags.%s' % sha_constructor(u).hexdigest()
    
def get_signature(token, contextable=False, comparison=False):
    """
    Gets the signature tuple for any native tag
    contextable searchs for ``as`` variable to update context
    comparison if true uses ``negate`` (p) to ``not`` the result (~p)
    returns (``tag_name``, ``args``, ``kwargs``)
    """
    # shelx.split has a bad habbit of inserting null bytes where they are not wanted
    bits = map(lambda bit: filter(lambda c: c != '\x00', bit), split(token.contents))
    args, kwargs = (), {}
    if comparison and bits[-1] == 'negate':
        kwargs['negate'] = True
        bits = bits[:-1]
    if contextable and len(bits) > 2 and bits[-2] == 'as':
        kwargs['varname'] = bits[-1]
        bits = bits[:-2]
    kwarg_re = re.compile(r'^([-\w]+)\=(.*)$')
    for bit in bits[1:]:
        match = kwarg_re.match(bit)
        if match:
            kwargs[match.group(1)] = force_unicode(match.group(2))
        else:
            args += (bit,)
    return bits[0], args, kwargs


class NativeNode(template.Node):
    bucket = None
    def __init__(self, parser, name, *args, **kwargs):
        self.parser = parser
        self.func = register[self.bucket][name]
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def get_args(self, context, resolve=True, apply_filters=True):
        args = (lookup(self.parser, var, context, resolve, apply_filters) for var in self.args)
        if hasattr(self.func, 'takes_context') and getattr(self.func, 'takes_context'):
            return (context,) + tuple(args)
        return args

    def get_kwargs(self, context, resolve=True, apply_filters=True):
        return dict(((k, lookup(self.parser, var, context, resolve)) for k, var in self.kwargs.items()))

    def render(self, context):
        resolve = getattr(self.func, 'resolve', True)
        apply_filters = getattr(self.func, 'apply_filters', True)
        kwargs = self.get_kwargs(context, resolve, apply_filters)
        varname = kwargs.pop('varname', None)
        
        def _get_result():
            result = self.get_result(context, *self.get_args(context, resolve, apply_filters), **kwargs)
            if hasattr(self.func, 'is_safe') and getattr(self.func, 'is_safe'):
                return mark_safe(result)
            return result
        
        if not DEFAULT_CACHE_TIMEOUT is None and not hasattr(self.func, 'cache'):
            setattr(self.func, 'cache', DEFAULT_CACHE_TIMEOUT)

        if hasattr(self.func, 'cache'):
            key = get_cache_key(self.bucket, self.name, self.args, self.kwargs)
            result = cache.get(key)
            if result is None:
                result = _get_result()
                cache.set(key, result, getattr(self.func, 'cache'))
        else:
            result = _get_result()

        if varname:
            context[varname] = result
            return ''
        
        return result
    
    def get_result(self, context):
        raise NotImplementedError

class ComparisonNode(NativeNode):
    bucket = 'comparison'
    def get_result(self, context, *args, **kwargs):
        nodelist_false = kwargs.pop('nodelist_false')
        nodelist_true = kwargs.pop('nodelist_true')
        negate = kwargs.pop('negate', False)
        
        try:
            truth_value = self.func(*args, **kwargs)
        except TypeError:
            # If the types don't permit comparison, return nothing.
            return ''

        if truth_value and negate:
            return nodelist_false.render(context)
        elif truth_value:
            return nodelist_true.render(context)
        elif negate:
            return nodelist_true.render(context)
        else:
            return nodelist_false.render(context)

def do_comparison(parser, token):
    """
    Compares passed arguments. 
    Attached functions should return boolean ``True`` or ``False``.
    If the attached function returns ``True``, the first node list is rendered.
    If the attached function returns ``False``, the second optional node list is rendered (part after the ``{% else %}`` statement). 
    If the last argument in the tag is ``negate``, then the opposite node list is rendered (like an ``ifnot`` tag).
    
    Syntax::

        {% if_[comparison] [var args...] [name=value kwargs...] [negate] %}
            {# first node list in here #}
        {% else %}
            {# second optional node list in here #}
        {% endif_[comparison] %}


    Supported comparisons are ``match``, ``find``, ``startswith``, ``endswith``,
    ``less``, ``less_or_equal``, ``greater`` and ``greater_or_equal`` and many more.
    Checkout the :ref:`contrib-index` for more examples

    Examples::

        {% if_less some_object.id 3 %}
        {{ some_object }} has an id less than 3.
        {% endif_less %}

        {% if_match request.path '^/$' %}
        Welcome home
        {% endif_match %}

    """
    name, args, kwargs = get_signature(token, comparison=True)
    name = name.replace('if_if', 'if')
    end_tag = 'end' + name
    kwargs['nodelist_true'] = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        kwargs['nodelist_false'] = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        kwargs['nodelist_false'] = template.NodeList()
    if name.startswith('if_'):
        name = name.split('if_')[1]
    return ComparisonNode(parser, name, *args, **kwargs)

class FunctionNode(NativeNode):
    bucket = 'function'
    def get_result(self, context, *args, **kwargs):
        result = self.func(*args, **kwargs)
        if hasattr(self.func, 'inclusion') and getattr(self.func, 'inclusion'):
            template_name, ctx = result
            if not isinstance(ctx, Context):
                ctx = Context(ctx)
            return get_template(template_name).render(ctx)
        return result

def do_function(parser, token):
    """
    Performs a defined function on the passed arguments.
    Normally this returns the output of the function into the template.
    If the second to last argument is ``as``, the result of the function is stored in the context and is named whatever the last argument is.

    Syntax::

        {% [function] [var args...] [name=value kwargs...] [as varname] %}

    Examples::

        {% search '^(\d{3})$' 800 as match %}

        {% map sha1 hello world %}

    """
    name, args, kwargs = get_signature(token, True, True)
    return FunctionNode(parser, name, *args, **kwargs)

class BlockNode(NativeNode):
    bucket = 'block'
    def get_result(self, context, *args, **kwargs):
        nodelist = kwargs.pop('nodelist', ())
        return self.func(context, nodelist, *args, **kwargs)

def do_block(parser, token):
    """
    Process several nodes inside a single block
    Block functions take ``context``, ``nodelist`` as first arguments
    If the second to last argument is ``as``, the rendered result is stored in the context and is named whatever the last argument is.

    Syntax::

        {% [block] [var args...] [name=value kwargs...] [as varname] %}
            ... nodelist ...
        {% end[block] %}

    Examples::

        {% render_block as rendered_output %}
            {{ request.path }}/blog/{{ blog.slug }}
        {% endrender_block %}

        {% highlight_block python %}
            import this
        {% endhighlight_block %}

    """
    name, args, kwargs = get_signature(token, contextable=True)
    kwargs['nodelist'] = parser.parse(('end%s' % name,))
    parser.delete_first_token()
    return BlockNode(parser, name, *args, **kwargs)
