import base64
from native_tags.decorators import function, filter

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
    
b16encode = codectag(16)
b16decode = codectag(16,False)
    
b32encode = codectag(32)
b32decode = codectag(32,False)
    
b64encode = codectag(64)
b64decode = codectag(64,False)
