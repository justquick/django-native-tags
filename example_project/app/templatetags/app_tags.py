from native_tags.decorators import function, comparison, filter
from datetime import datetime

def dynamic(*a, **kw):
    return list(a) + sorted(kw.items())
dynamic = function(dynamic)

def no_render(*a, **kw):
     return list(a) + sorted(kw.items())
no_render = function(no_render, resolve=False)

def myfilter(value, arg):
    return value + arg
myfilter = filter(myfilter, test={'args':(1,1),'result':2})
    
def adder(x, y):
    return x + y
adder = function(adder, name='add', test={'args':(1,1),'result':2})
    
def cmp_kwargs(**kw):
    return len(kw)
cmp_kwargs = comparison(cmp_kwargs)

def myinc(noun):
    return 'unittest.html', {'noun': noun}
myinc = function(myinc, inclusion=True)

def ifsomething():
    return True
ifsomething = comparison(ifsomething)

def date():
    return datetime.now()
date = function(date, cache=3600)

def fail():
    1/0
fail = function(fail, fallback='woot')