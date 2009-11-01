"""
Comparison tags
"""
try:
    set
except NameError:
    from sets import Set as set
from django.conf import settings
from native_tags.decorators import comparison

def less(x,y):
    'True if x is less than y'
    return x < y
less = comparison(less)

def less_or_equal(x,y):
    'True if x is less than or equal to y'
    return x <= y
less_or_equal = comparison(less_or_equal)

def greater_or_equal(x,y):
    'True if x is greater than or equal to y'
    return x >= y
greater_or_equal = comparison(greater_or_equal)

def greater(x,y):
    'True if x is greater than y'
    return x > y
greater = comparison(greater)
    
def startswith(x,y):
    'String comparison. True if x startswith y'
    return x.startswith(y)
startswith = comparison(startswith)

def endswith(x,y):
    'String comparison. True if x endswith y'
    return x.endswith(y)
endswith = comparison(endswith)

def contains(x,y):
    'String comparison. True if x contains y anywhere'
    return x.find(y) > -1
contains = comparison(contains)

def subset(x,y):
    'Set comparison. True if x is a subset of y'
    return set(x) <= set(y)
subset = comparison(subset)

def superset(x,y):
    'Set comparison. True if x is a superset of y'
    return set(x) >= set(y)
superset = comparison(superset)

def divisible_by(x,y):
    'Numeric comparison. True if x is divisible by y'
    return float(x) % float(y) == 0
divisible_by = comparison(divisible_by)

def setting(x):
    'True if setting x is defined in your settings'
    return hasattr(settings, x)
setting = comparison(setting)

