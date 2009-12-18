try:
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name
    from pygments import highlight as highlighter
except ImportError:
    highlighter = None

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
    if highlighter is None:
        return ''
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

            {% highlight 'print "Hello World"' python linenos=true %}
    """
    if highlighter is None:
        return '<pre>%s</pre>' % code
    return highlighter(code or '', get_lexer_by_name(lexer), HtmlFormatter(**kwargs))
highlight = function(highlight, is_safe=True)

def highlight_block(context, nodelist, lexer, **kwargs):
    """
    Code is nodelist ``rendered`` in ``context``
    Returns highlighted code ``div`` tag from ``HtmlFormatter``
    Lexer is guessed by ``lexer`` name
    arguments are passed into the formatter

        Syntax::

            {% highlight_block [lexer name] [formatter options] %}
                ... source code ..
            {% endhighlight_block %}

        Example::

            {% highlight_block python linenos=true %}
                print '{{ request.path }}'
            {% endhighlight_block %}
    """
    if highlighter is None:
        return '<pre>%s</pre>' % str(nodelist.render(context) or '')
    return highlighter(nodelist.render(context) or '', get_lexer_by_name(lexer), HtmlFormatter(**kwargs))
highlight_block = block(highlight_block, is_safe=True)
