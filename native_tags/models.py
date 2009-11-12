import settings

if settings.LOAD:
    from django.template import add_to_builtins
    add_to_builtins('native_tags.templatetags.native')
