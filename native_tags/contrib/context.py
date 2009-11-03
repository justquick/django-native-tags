from native_tags.decorators import function, block, filter

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
do_del = function(do_del, do_not_resolve = 1, takes_context=1, name='del')


def render_block(context, nodelist):
    'Simply renders the nodelist with the current context'
    return nodelist.render(context)
render_block = block(render_block)
