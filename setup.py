from setuptools import setup, find_packages
from native_tags import __version__

try:
    readme = open('README.rst').read()
except IOError:
    readme = ''

setup(name='django-native-tags',
    version=__version__,
    description='Native, Pythonic Templatetags for Django',
    long_description=readme,
    author='Justin Quick',
    author_email='justquick@gmail.com',
    url='http://github.com/justquick/django-native-tags',
    packages=find_packages(exclude=('example_project',)),
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    )
