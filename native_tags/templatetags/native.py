from django.template import Library

from native_tags.nodes import do_function, do_comparison, do_block
from native_tags.registry import register as native_register


register = Library()

for tag_name in native_register['comparison']:
    if not tag_name.startswith('if'):
        tag_name = 'if_%s' % tag_name 
    register.tags[tag_name] = do_comparison
    
for tag_name in native_register['function']:
    register.tags[tag_name] = do_function

for tag_name in native_register['block']:
    register.tags[tag_name] = do_block

register.filters.update(native_register['filter'])