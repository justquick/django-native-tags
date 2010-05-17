import operator
from native_tags.decorators import comparison, function

# Comparison operators

def lt(a, b):
    return operator.lt(a, b)
lt = comparison(lt, doc=operator.lt.__doc__)
    
def le(a, b):
    return operator.le(a, b)
le = comparison(le, doc=operator.le.__doc__)
    
def eq(a, b):
    return operator.eq(a, b)
eq = comparison(eq, doc=operator.eq.__doc__)
    
def ne(a, b):
    return operator.ne(a, b)
ne = comparison(ne, doc=operator.ne.__doc__)
    
def ge(a, b):
    return operator.ge(a, b)
ge = comparison(ge, doc=operator.ge.__doc__)
    
def gt(a, b):
    return operator.gt(a, b)
gt = comparison(gt, doc=operator.gt.__doc__)

def not_(a):
    return operator.not_(a)
not_ = comparison(not_, name='not', doc=operator.not_.__doc__)

def is_(a):
    return operator.is_(a)
is_ = comparison(is_, name='is', doc=operator.is_.__doc__)

def is_not(a):
    return operator.is_not(a)
is_not = comparison(is_not, doc=operator.is_not.__doc__)

# Mathematical and bitwise operators

def abs(a):
    return operator.abs(a)
abs = function(comparison(abs), doc=operator.abs.__doc__)

def add(a, b):
    return operator.add(a, b)
add = function(add, doc=operator.add.__doc__)
    
def and_(a, b):
    return operator.and_(a, b)
and_ = function(comparison(and_, name='and'), doc=operator.and_.__doc__)

def div(a, b):
    return operator.div(a, b)
div = function(comparison(div), doc=operator.div.__doc__)
    
def floordiv(a, b):
    return operator.floordiv(a, b)
floordiv = function(comparison(floordiv), doc=operator.floordiv.__doc__)

def index(a):
    return operator.index(a)
index = function(comparison(index), doc=operator.index.__doc__)

def inv(a):
    return operator.inv(a)
inv = function(comparison(inv), doc=operator.inv.__doc__)
    
def lshift(a, b):
    return operator.lshift(a, b)
lshift = function(comparison(lshift), doc=operator.lshift.__doc__)
    
def mod(a, b):
    return operator.mod(a, b)
mod = function(comparison(mod), doc=operator.mod.__doc__)
    
def mul(a, b):
    return operator.mul(a, b)
mul = function(comparison(mul), doc=operator.mul.__doc__)
    
def neg(a):
    return operator.neg(a)
neg = function(comparison(neg), doc=operator.neg.__doc__)
    
def or_(a, b):
    return operator.or_(a, b)
or_ = function(comparison(or_), doc=operator.or_.__doc__)
    
def pos(a):
    return operator.pos(a)
pos = function(comparison(pos), doc=operator.pos.__doc__)
    
def pow(a, b):
    return operator.pow(a, b)
pow = function(comparison(pow), doc=operator.pow.__doc__)
    
def rshift(a, b):
    return operator.rshift(a, b)
rshift = function(comparison(rshift), doc=operator.rshift.__doc__)
    
def sub(a, b):
    return operator.sub(a, b)
sub = function(comparison(sub), doc=operator.sub.__doc__)
    
def truediv(a, b):
    return operator.truediv(a, b)
truediv = function(comparison(truediv), doc=operator.truediv.__doc__)
    
def xor(a, b):
    return operator.xor(a, b)
xor = function(comparison(xor), doc=operator.xor.__doc__)
    
# Sequence operators
    
def concat(a, b):
    return operator.concat(a, b)
concat = function(concat, doc=operator.concat.__doc__)

def contains(a, b):
    return operator.contains(a, b)
contains = function(contains, doc=operator.contains.__doc__)
    
def countOf(a, b):
    return operator.countOf(a, b)
countOf = function(countOf, doc=operator.countOf.__doc__)
    
def delitem(a, b):
    return operator.delitem(a, b)
delitem = function(delitem, doc=operator.delitem.__doc__)
    
def delslice(a, b, c):
    return operator.delslice(a, b, c)
delslice = function(delslice, doc=operator.delslice.__doc__)
    
def getitem(a, b):
    return operator.getitem(a, b)
getitem = function(getitem, doc=operator.getitem.__doc__)
    
def getslice(a, b, c):
    return operator.getslice(a, b, c)
getslice = function(getslice, doc=operator.getslice.__doc__)
    
def indexOf(a, b):
    return operator.indexOf(a, b)
indexOf = function(indexOf, doc=operator.indexOf.__doc__)
    
def repeat(a, b):
    return operator.repeat(a, b)
repeat = function(repeat, doc=operator.repeat.__doc__)
    
def setitem(a, b, c):
    return operator.setitem(a, b, c)
setitem = function(setitem, doc=operator.setitem.__doc__)
    
def setslice(a, b, c, v):
    return operator.setslice(a, b, c, v)
setslice = function(setslice, doc=operator.setslice.__doc__)
