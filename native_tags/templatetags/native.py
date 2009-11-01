from django.template import Library
from native_tags.nodes import do_function, do_comparison, do_block
from native_tags import register as native_register


register = Library()

for tag_name in native_register['comparison']:
    register.tag('if_%s' % tag_name, do_comparison)
    
for tag_name in native_register['function']:
    register.tag(tag_name, do_function)

for name,filter_func in native_register['filter'].items():
    register.filter(name, filter_func)

for tag_name in native_register['block']:
    register.tag(tag_name, do_block)
