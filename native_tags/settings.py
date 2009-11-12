from django.conf import settings

TAG_TYPES = ('function', 'comparison', 'filter', 'block')
LOAD = getattr(settings, 'NATIVE_LOAD', True)

LIBRARY = getattr(settings, 'NATIVE_LIBRARY', {})

CONTRIB = getattr(settings, 'NATIVE_CONTRIB', (
    'native_tags.contrib.comparison',
    'native_tags.contrib.context',
    'native_tags.contrib.generic_content',
    'native_tags.contrib.generic_markup',
    'native_tags.contrib.hash',
    'native_tags.contrib.serializers',
    'native_tags.contrib.baseencode',
    'native_tags.contrib.regex',
    'native_tags.contrib.mapreduce',    
    'native_tags.contrib.cal',
    'native_tags.contrib.rand',
        
    # Tags that have dependencies
    'native_tags.contrib.gchart', # GChartWrapper
    'native_tags.contrib.pygmentize', # Pygments
    'native_tags.contrib.feeds', # Feedparser
    
    # Implementation of ``django.template.defaulttags`` in native_tags
    # not really usefull, just proof of concept
    #'native_tags.contrib._django',
))

BUILTIN_TAGS = getattr(settings, 'DJANGO_BUILTIN_TAGS', (
    #'django.contrib.markup.templatetags.markup,
))
