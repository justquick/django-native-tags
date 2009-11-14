import settings

if 'native_tags.templatetags.native' in settings.BUILTIN_TAGS:
    from django.template import add_to_builtins
    add_to_builtins('native_tags.templatetags.native')
