from distutils.core import setup
from native_tags import __version__

setup(name='django-native-tags',
    version=__version__,
    description='Native, Pythonic Templatetags for Django',
    long_description=open('README.rst').read(),
    author='Justin Quick',
    author_email='justquick@gmail.com',
    url='http://github.com/justquick/django-native-tags',
    packages=['native_tags', 'native_tags.contrib', 'native_tags.templatetags'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    )
