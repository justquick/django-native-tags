Native Tags Documentation
=========================

:Authors:
   Justin Quick <justquick@gmail.com>
:Version: 0.3

Django Native Tags is a way of making the creation of template tags stupidly simple.
Tags are "native" because there is a much closer relationship between the tag in the template and a Python function behind the scenes.
The app abstracts the work needed to parse out the templatetag syntax into a useable form for a Python function.
For example:

Define an arbitrary function in your templatetags::

   def add(x, y):
      return x + y
   add.function = True
   
Use the function in your template::

   {% add 1000 100 as num %}
   {{ num|intcomma }}

Which outputs::

   1,100
   
Other features of Native Tags:
 
 * Keyword argument parsing
 * Quoted strings parsed correctly
 * Add templatetags to Django's builtins (no ``{% load %}`` required)
 * Auto resolve of template variables
 * Universal and per-tag caching

The real power of the module comes in the contrib add ons which has tons of tags for various uses including
comparisons, regex operations, math operations, and much more. By default it is a functional replacement to `James Bennett`_'s `django-template-utils`_ right out of the box

.. _django-template-utils: http://bitbucket.org/ubernostrum/django-template-utils/
.. _James Bennett: http://www.b-list.org/

For full documentation, checkout the `fancy Sphinx doc`_

.. _fancy Sphinx doc: http://justquick.github.com/django-native-tags/

Email me with any questions/concerns/issues/hate mail:

   justquick [@] the gmails .com
