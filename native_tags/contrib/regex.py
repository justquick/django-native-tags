import re

from native_tags.decorators import comparison, function


def matches(pattern, text):
    'String comparison. True if string ``text`` matches regex ``pattern``'
    return re.compile(str(pattern)).match(text)
matches = comparison(matches)

def substitute(search, replace, text):
    'Regex substitution function. Replaces regex ``search`` with ``replace`` in ``text``'
    return re.sub(re.compile(str(search)), replace, text)
substitute = function(substitute)

def search(pattern, text):
    'Regex pattern search. Returns match if ``pattern`` is found in ``text``'
    return re.compile(str(pattern)).search(str(text))
search = function(search)
