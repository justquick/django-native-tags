from django.template import add_to_builtins
import settings

if settings.LOAD:
    add_to_builtins('native_tags.templatetags.native')
