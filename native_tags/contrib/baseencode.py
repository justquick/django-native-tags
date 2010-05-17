import base64
from native_tags.decorators import function, filter
from hashlib import sha1

def codectag(encoding, codec=True):
    codec = 'b%d%s' % (encoding, codec and 'encode' or 'decode')
    def inner(s, *args, **kwargs):
        return getattr(base64, codec)(s, *args, **kwargs)
    inner.__name__ = codec 
    inner.__doc__ = getattr(base64, codec).__doc__ + """

Syntax::
    
    {%% %s [string] [options] %%}
    """ % codec
    return filter(function(inner))

enc,dec = '1','31'
b16encode = codectag(16)
b16encode.test = {'args':(enc,),'result':dec}
b16decode = codectag(16,False)
b16decode.test = {'args':(dec,),'result':enc}
    
enc,dec = 'z','PI======'
b32encode = codectag(32)
b32encode.test = {'args':(enc,),'result':dec}
b32decode = codectag(32,False)
b32decode.test = {'args':(dec,),'result':enc}
    
enc,dec = 'z','eg=='
b64encode = codectag(64)
b64encode.test = {'args':(enc,),'result':dec}
b64decode = codectag(64,False)
b64decode.test = {'args':(dec,),'result':enc}
