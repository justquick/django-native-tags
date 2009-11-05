import settings

def tag(bucket,doc):
    def wrapped(inner, **options):
        options[bucket] = 1
        if 'name' in options:
            inner.__name__ = inner.name = options.pop('name')
        if 'doc' in options:
            inner.__doc__ = inner.doc = options.pop('doc')
        for i in options.items():
            setattr(inner, *i)
        newdoc = ''.join([
            'This is a :ref:`%s tag<%s-tags>`. ' % (tag,tag)
            for tag in settings.TAG_TYPES
            if hasattr(inner,tag) and
              str(inner.__doc__).find('This is a :ref:`%s'%tag)==-1])
        inner.__doc__ = inner.doc = '%s\n\n%s' % (newdoc, inner.__doc__)
        return inner
    wrapped.__doc__ = doc
    return wrapped

block = tag('block', """
Block tag function decorator

Syntax::

    @block([**options])
    def my_tag_function(context, nodelist, [*vars], [**tag_options]):
        return nodelist.render(context)
""")
comparison = tag('comparison',"""
Comparison tag function decorator

Syntax::

    @comparison([**options]):
    def my_comparison([*vars], [**tag_options]):
        return True
""")
comparison.__doc__
filter = tag('filter',"""
Filter tag function decorator

Syntax::

    @filter([**options]):
    def my_filter(value, *args):
        return value
""")
function = tag('function',"""
Function tag function decorator

Syntax::

    @filter([**options]):
    def my_function([*args], [**kwargs]):
        return args, kwargs
""")
