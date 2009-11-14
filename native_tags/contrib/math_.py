import math

from native_tags.decorators import function, filter, comparison

def func_factory(method):
    try:
        func = getattr(math, method)
    except AttributeError:
        return
    def inner(arg1, arg2=None):
        try:
            return func(arg1, arg2)
        except TypeError:
            return func(arg1)
    inner.__name__ = method
    doc = func.__doc__.splitlines()
    if len(doc) > 1 and not doc[1]:
        doc = doc[2:]
    inner.__doc__ = '\n'.join(doc)
    if method.startswith('is'):
        return comparison(inner)
    return filter(function(inner))


acos = func_factory('acos')
acosh = func_factory('acosh')
asin = func_factory('asin')
asinh = func_factory('asinh')
atan = func_factory('atan')
atan2 = func_factory('atan2')
atanh = func_factory('atanh')
ceil = func_factory('ceil')
copysign = func_factory('copysign')
cos = func_factory('cos')
cosh = func_factory('cosh')
degrees = func_factory('degrees')
exp = func_factory('exp')
fabs = func_factory('fabs')
factorial = func_factory('factorial')
floor = func_factory('floor')
fmod = func_factory('fmod')
frexp = func_factory('frexp')
fsum = func_factory('fsum')
hypot = func_factory('hypot')
isinf = func_factory('isinf')
isnan = func_factory('isnan')
ldexp = func_factory('ldexp')
log = func_factory('log')
log10 = func_factory('log10')
log1p = func_factory('log1p')
modf = func_factory('modf')
pow = func_factory('pow')
radians = func_factory('radians')
sin = func_factory('sin')
sinh = func_factory('sinh')
sqrt = func_factory('sqrt')
tan = func_factory('tan')
tanh = func_factory('tanh')
trunc = func_factory('trunc')
