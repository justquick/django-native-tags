from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments import highlight as highlighter

from native_tags.decorators import function, block

def highlight_style(cssclass='highlight', **kwargs):
    """
    Returns the CSS from the ``HtmlFormatter``.
    ``cssclass`` is the name of the ``div`` css class to use
    
        Syntax::
            
            {% highlight_style [cssclass] [formatter options] %}
            
        Example::
            
            {% highlight_style code linenos=true %}
    """
    return HtmlFormatter(**kwargs).get_style_defs('.%s' % cssclass)    
highlight_style = function(highlight_style)

def highlight(code, lexer, **kwargs):
    """
    Returns highlighted code ``div`` tag from ``HtmlFormatter``
    Lexer is guessed by ``lexer`` name
    arguments are passed into the formatter
    
        Syntax::
            
            {% highlight [source code] [lexer name] [formatter options] %}
            
        Example::
            
            {% highlight_style 'print "Hello World"' python linenos=true %}
    """
    try:
        return highlighter(code, get_lexer_by_name(lexer), HtmlFormatter(**kwargs))
    except:
        return ''
highlight = function(highlight)

def block_highlight(context, nodelist, lexer, **kwargs):
    """
    Code is nodelist ``rendered`` in ``context``
    Returns highlighted code ``div`` tag from ``HtmlFormatter``
    Lexer is guessed by ``lexer`` name
    arguments are passed into the formatter
    
        Syntax::
            
            {% block_highlight [lexer name] [formatter options] %}
                ... source code ..
            {% endblock_highlight %}
            
        Example::
            
            {% block_highlight python linenos=true %}
                print '{{ request.path }}'
            {% endblock_highlight %}
    """
    try:
        return highlighter(nodelist.render(context), get_lexer_by_name, HtmlFormatter(**kwargs))
    except:
        return ''
block_highlight = block(block_highlight)
