from django.conf import settings as djsettings
from django.template import add_to_builtins
from django.utils.importlib import import_module
from os import listdir
import settings


class AlreadyRegistered(Exception):
    "The function you are trying to register is already in the registry"
    pass

class NotRegistered(Exception):
    "The function you are trying to unregister is not in the registry"
    pass

class Library(dict):
    """
    A simple dictionary with register and unregister functions
    """
    def __init__(self):
        super(Library, self).__init__([(tag, {}) for tag in settings.TAG_TYPES])
        self.update([i for i in settings.LIBRARY.items() if i[0] in settings.TAG_TYPES])

    def register(self, bucket, name_or_func, func=None):
        """
        Add a function to the registry by name
        """
        assert bucket in self, 'Bucket %s is unknown' % bucket
        if func is None and hasattr(name_or_func, '__name__'):
            name = name_or_func.__name__
            func = name_or_func
        elif func:
            name = name_or_func
        if name in self[bucket]:
            raise AlreadyRegistered('The function %s is already registered' % name)

        self[bucket][name] = func

    def unregister(self, bucket, name):
        """
        Remove the function from the registry by name
        """
        assert bucket in self, 'Bucket %s is unknown' % bucket
        if not name in self[bucket]:
            raise NotRegistered('The function %s is not registered' % name)
        del self[bucket][name]

    def function(self, *a, **kw):
        self.register('function', *a, **kw)

    def comparison(self, *a, **kw):
        self.register('comparison', *a, **kw)

    def filter(self, *a, **kw):
        self.register('filter', *a, **kw)

    def block(self, *a, **kw):
        self.register('block', *a, **kw)

    def get_doc(self, tag_name):
        "Get documentation for the first tag matching the given name"
        for tag,func in self.tags:
            if tag.startswith(tag_name) and func.__doc__:
                return func.__doc__

    def get_bucket(self, name):
        "Find out which bucket a given tag name is in"
        for bucket in self:
            for k,v in self[bucket].items():
                if k == name:
                    return bucket

    def get(self, name):
        "Get the first tag function matching the given name"
        for bucket in self:
            for k,v in self[bucket].items():
                if k == name:
                    return v
                
    def tags(self):
        "Iterate over all tags yielding (name, function)"
        for bucket in self:
            for k,v in self[bucket].items():
                yield k,v
    tags = property(tags)

    def __len__(self):
        return reduce(lambda x,y: x+y, map(len, self.values()))

register = Library()

def load_module(module):
    """
    Load a module string like django.contrib.markup.templatetags.markup into the registry
    Iterates through the module looking for callables w/ attributes matching Native Tags
    """
    global register
    if isinstance(module, basestring) and module.find('.') > -1:
        a = module.split('.')
        module = ('.%s' % a[-1], '.'.join(a[:-1]))
    try:
        module = import_module(*module)
    except:
        return
    for name in dir(module):
        if name.startswith('_'): continue
        obj = getattr(module, name)
        if callable(obj):
            for tag in settings.TAG_TYPES:
                if hasattr(obj, tag) and getattr(obj, tag) in (1, True):
                    name = getattr(obj, 'name', obj.__name__)
                    if name in register[tag]:
                        continue
                    if hasattr(obj, 'name'):
                        register.register(tag, getattr(obj, 'name'), obj)
                    else:
                        register.register(tag, obj)


# Load up the native contrib tags
map(load_module, settings.TAGS)

# Add the BUILTIN_TAGS to Django's builtins
for mod in settings.BUILTIN_TAGS:
    # if it tries to add iself in here it blows up really badly
    # this part is done in models.py
    if mod != 'native_tags.templatetags.native':
        add_to_builtins(mod)

