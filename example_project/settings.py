import sys, os

# Quick hack to put native_tags from the parent directory into pythonpath
sys.path.append(
    os.path.abspath(
        os.path.normpath('%s/../' % os.path.dirname(__file__))
    )
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'test.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wlk%thwka5=lfl(d7qfb((u7j=$!(%h-!(ci6tte)y=b1&evtb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'example_project.urls'

TEMPLATE_DIRS = (
    'templates',
)

CACHE_BACKEND = 'locmem://'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'native_tags',
    'app',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)


NATIVE_TAGS = (
    # Extra native contrib tags to test
    'native_tags.contrib.comparison',
    'native_tags.contrib.context',
    'native_tags.contrib.generic_content',
    'native_tags.contrib.generic_markup',
    'native_tags.contrib.hash',
    'native_tags.contrib.serializers',
    'native_tags.contrib.baseencode',
    'native_tags.contrib.regex',
    'native_tags.contrib.mapreduce',    
    'native_tags.contrib.cal',
    'native_tags.contrib.math_',
    'native_tags.contrib.rand',
        
    # Native tags with dependencies
    'native_tags.contrib.gchart', # GChartWrapper
    'native_tags.contrib.pygmentize', # Pygments
    'native_tags.contrib.feeds', # Feedparser
)

DJANGO_BUILTIN_TAGS = (
    'native_tags.templatetags.native',
    'django.contrib.markup.templatetags.markup',
)

MARKUP_FILTER = ('markdown', { 'safe_mode': True })

try:
    import markdown
    INSTALLED_APPS += ('django.contrib.markup',)
except ImportError:
    pass

try:
    import django_coverage
    TEST_RUNNER = 'django_coverage.coverage_runner.run_tests'
except ImportError:
    pass