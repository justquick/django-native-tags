from django.conf import settings

TAG_TYPES = ('function', 'comparison', 'filter', 'block')

LIBRARY = getattr(settings, 'NATIVE_LIBRARY', {})

TAGS = getattr(settings, 'NATIVE_TAGS', (
    'native_tags.contrib.comparison',
    'native_tags.contrib.generic_content',
    'native_tags.contrib.generic_markup',
    'native_tags.contrib.feeds', # Feedparser
))

BUILTIN_TAGS = getattr(settings, 'DJANGO_BUILTIN_TAGS', ())

DEFAULT_CACHE_TIMEOUT = getattr(settings, 'NATIVE_DEFAULT_CACHE_TIMEOUT', None)