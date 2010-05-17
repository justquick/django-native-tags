from native_tags.decorators import function

def get_func(func_name, op=True):
    import operator
    from native_tags.registry import register
    try:
        return register['function'][func_name]
    except KeyError:
        pass
    if func_name in __builtins__:
        return __builtins__[func_name]
    elif hasattr(operator, func_name):
        return getattr(operator, func_name)
    return lambda: None
    
def do_map(func_name, *sequence):
    """
    Return a list of the results of applying the function to the items of
    the argument sequence(s).  
    
    Functions may be registered with ``native_tags`` 
    or can be ``builtins`` or from the ``operator`` module
    
    If more than one sequence is given, the
    function is called with an argument list consisting of the corresponding
    item of each sequence, substituting None for missing values when not all
    sequences have the same length.  If the function is None, return a list of
    the items of the sequence (or a list of tuples if more than one sequence).

    Syntax::
    
        {% map [function] [sequence] %}        
        {% map [function] [item1 item2 ...] %}

    For example::
    
        {% map sha1 hello world %}
        
    calculates::
        
        [sha1(hello), sha1(world)]

    """

    if len(sequence)==1:
        sequence = sequence[0]
    return map(get_func(func_name, False), sequence)
do_map = function(do_map, name='map')
do_map.test = {'args':('ord','wtf'),'result':[119, 116, 102]}

def do_reduce(func_name, *sequence):
    """
    Apply a function of two arguments cumulatively to the items of a sequence,
    from left to right, so as to reduce the sequence to a single value.
    
    Functions may be registered with ``native_tags`` 
    or can be ``builtins`` or from the ``operator`` module
    
    Syntax::
    
        {% reduce [function] [sequence] %}        
        {% reduce [function] [item1 item2 ...] %}
    
    For example::
    
        {% reduce add 1 2 3 4 5 %}
        
    calculates::
    
        ((((1+2)+3)+4)+5) = 15
    """
    if len(sequence)==1:
        sequence = sequence[0]
    return reduce(get_func(func_name), sequence)
do_reduce = function(do_reduce, name='reduce')
do_reduce.test = {'args':('add',1,2,3,4,5),'result':15}
