from django.template import Library
from native_tags.nodes import do_function, do_comparison, do_block
from native_tags.registry import load_module, AlreadyRegistered, register as native_register
from django.conf import settings
from django.utils.importlib import import_module
from os import listdir

register = Library()

# Comb through installed apps w/ templatetags looking for native tags
for app in settings.INSTALLED_APPS :
    if app == 'native_tags':
        continue
    try:
        mod = import_module('.templatetags', app)
    except ImportError:
        continue

    # TODO: Make this hurt less
    for f in listdir(mod.__path__[0]):
        if f.endswith('.py') and not f.startswith('__'):
            try:
                load_module('%s.templatetags.%s' % (app,f.split('.py')[0]))
            except AlreadyRegistered:
                break
            except ImportError:
                continue

for tag_name in native_register['comparison']:
    if not tag_name.startswith('if'):
        tag_name = 'if_%s' % tag_name 
    register.tags[tag_name] = do_comparison
    
for tag_name in native_register['function']:
    register.tags[tag_name] = do_function

for tag_name in native_register['block']:
    register.tags[tag_name] = do_block

register.filters.update(native_register['filter'])