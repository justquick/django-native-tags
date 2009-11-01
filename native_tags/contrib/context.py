from native_tags.decorators import function, block, filter

def document(f):
    return f.__doc__
document = filter(document)

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


def render(context, nodelist):
    'Simply renders the nodelist with the current context'
    return nodelist.render(context)
render = block(render)
