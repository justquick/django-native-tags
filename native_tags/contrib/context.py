from native_tags.decorators import function, block, filter
from django.template import Template, Context


def document(o):
    'Returns the docstring for a given object'
    try:
        return o.__doc__ or ''
    except AttributeError:
        return ''
document = filter(function(document))

def do_set(context, **kwargs):
    'Updates the context with the keyword arguments'
    context.update(kwargs)
    return ''
do_set = function(do_set, takes_context=1, name='set')


def do_del(context, *args):
    'Deletes template variables from the context'
    for name in args:
        del context[name]
    return ''
do_del = function(do_del, resolve=0, takes_context=1, name='del')


def render_block(context, nodelist):
    'Simply renders the nodelist with the current context'
    return nodelist.render(context)
render_block = block(render_block)


def template_string(context, template):
    'Return the rendered template content with the current context'
    if not isinstance(context, Context):
        context = Context(context)
    return Template(template).render(context)
template_string = function(template_string, takes_context=1)
template_string.test = {'args':({'var':'T'},'W {{ var }} F'),'result':'W T F'}

def template_block(context, nodelist):
    'Return the rendered block\'s content with the current context'
    return Template(nodelist.render(context)).render(context)
template_block = block(template_block)

def native_debug():
    from native_tags.registry import register
    return register
native_debug = function(native_debug)