Native Tags Documentation
=========================

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
 * Quoted strings parsed corectly
 * No ``{% load %}`` tags required
 * Auto resolve of template variables

The real power of the module comes in the Contrib Add Ons which has tons of tags right out of the box, ready to use.
Proper use of the Contrib Add Ons makes this app a functional replacement to `James Bennett`_'s `django-template-utils`_

.. _django-template-utils: http://bitbucket.org/ubernostrum/django-template-utils/
.. _James Bennett: http://www.b-list.org/

For full documentation, checkout the `fancy Sphinx doc`_

.. _fancy Sphinx doc: http://justquick.gitpages.com/django-native-tags/

Email me with any questions/concerns/issues/hate mail:

   justquick [@] the gmails .com