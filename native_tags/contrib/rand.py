import random as _random
from native_tags.decorators import function

def randrange(*args,**kwargs):
    if len(args)==1:
        args = (0,args[0])
    return _random.randrange(*args,**kwargs)
randrange = function(randrange)
randrange.__doc__ = _random.randrange.__doc__ + """

    Syntax::
        
        {% randrange [stop] [options] %}
        {% randrange [start] [stop] [step] [options] %}
"""

def randint(a, b):
    return _random.randint(a, b)
randint = function(randint)
randint.__doc__ = _random.randint.__doc__ + """

    Syntax::
        
        {% randint [a] [b] %}
"""

def randchoice(*seq):
    if len(seq)==1:
        seq = seq[0]
    return _random.choice(seq)
randchoice = function(randchoice)
randchoice.__doc__ = _random.choice.__doc__ + """

    Syntax::
        
        {% randchoice [sequence] %}
        {% randchoice [choice1 choice2 ...] %}
"""

def random():
    return _random.random()
random = function(random)
random.__doc__ = _random.random.__doc__ + """

    Syntax::
        
        {% random %}
"""

