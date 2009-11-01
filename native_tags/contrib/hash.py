from django.utils.hashcompat import md5_constructor, sha_constructor
from native_tags.decorators import function, filter

def hexd(algo, value):
    lookup = {
        'md5': md5_constructor,
        'sha1': sha_constructor,
        'sha': sha_constructor,
    }
    try:
        import hashlib
        lookup.update({
            'sha224': hashlib.sha224,
            'sha256': hashlib.sha256,
            'sha384': hashlib.sha384,
            'sha512': hashlib.sha512,
        })
    except ImportError:
        pass
    try:
        return lookup[algo](value).hexdigest()
    except IndexError:
        return ''

def hashtag(algo):
    def inner(value):
        return hexd(algo, value)
    return filter(function(inner),doc='Returns %s hexadecimal hash of the value' % algo.upper(),name=algo)
    
md5 = hashtag( 'md5')
sha1 = hashtag('sha1')
sha224 = hashtag('sha224')
sha256 = hashtag('sha256')
sha384 = hashtag('sha384')
sha512 = hashtag('sha512')
