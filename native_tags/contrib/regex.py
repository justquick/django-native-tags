import re

from native_tags.decorators import comparison, function


def matches(pattern, text):
    'String comparison. True if string ``text`` matches regex ``pattern``'
    return re.compile(str(pattern)).match(text)
matches = comparison(matches)
matches.test = {'args':('\d','_'),'result':None}

def substitute(search, replace, text):
    'Regex substitution function. Replaces regex ``search`` with ``replace`` in ``text``'
    return re.sub(re.compile(str(search)), replace, text)
substitute = function(substitute)
substitute.test = {'args':('w','f','wtf'),'result':'ftf'}

def search(pattern, text):
    'Regex pattern search. Returns match if ``pattern`` is found in ``text``'
    return re.compile(str(pattern)).search(str(text))
search = function(search)
search.test = {'args':('\d','asdfasdfwe'),'result':None}
