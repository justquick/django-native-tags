from distutils.core import setup


setup(name='django-native-tags',
      version='0.1',
      description='Pythonic Templatetags for Django',
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
