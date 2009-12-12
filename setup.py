from distutils.core import setup


setup(name='django-native-tags',
      version='0.2',
      description='Native, Pythonic Templatetags for Django',
      long_description=open('README.rst').read(),
      author='Justin Quick',
      author_email='justquick@gmail.com',
      url='http://github.com/justquick/django-native-tags',
      packages=['native_tags', 'native_tags.contrib', 'native_tags.templatetags'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
