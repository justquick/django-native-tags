from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase
from django.conf import settings as djsettings
from django.core.serializers import deserialize

from native_tags import settings, register
import atexit
import datetime
import os

TAG_TEMPLATE = """
{% if_contains name 'calendar' negate %}
<div>
    <h1><a onclick="document.getElementById('doc{{ name }}').style.display = 'block';">{{ name }}</a></h1>
    <pre id="doc{{ name }}" style="display: none;">
    {{ doc }}
    </pre>
    <div style="background: #FFFFCC none repeat scroll 0 0;">
    {{ src }}
    &nbsp;</div>  
    <div style="background-color: {% if error %}red{% else %}green{% endif %}">
    {% if error %}{{ error }}{% else %}{{ bit }}{% endif %}
    &nbsp;</div>
</div><hr>
{% endif_contains %}
"""

try:
    import pygments
    TAG_TEMPLATE = TAG_TEMPLATE.replace('{{ doc }}','{% highlight doc rest %}')
except ImportError:
    pygments = None

TESTFILE = 'media/index.html'

if os.path.isfile(TESTFILE):
    os.remove(TESTFILE)

TESTFILE = open(TESTFILE,'a')
atexit.register(TESTFILE.close)

if pygments:
    TESTFILE.write(Template('<style>{% highlight_style %}</style>').render(Context()))

class TemplateTest(TestCase):


    def render(self, src, ctx=None, err=None):
        name = repr(self).split('testMethod=')[1].split('>')[0][5:]
        try:
            bit = Template(src).render(Context(ctx))
        except Exception, e:
            if not djsettings.DEBUG:
                bit = ''
                err = e
            else:
                raise
        TESTFILE.write(Template(TAG_TEMPLATE).render(Context({
            'name':name, 'doc':register.get_doc(name), 'src':src, 'bit':bit, 'error':err,
        })))
        return bit

    def setUp(self):
        self.test_user = User.objects.create(username='tester',email='test')
        self.hash = {'foo':'bar'}
        
        self.tags = {}

    def test_less(self):
        t = """{% if_less 1 2 %}y{% endif_less %}{% if_less_or_equal 1 2 %}y{% endif_less_or_equal %}{% if_greater 2 1 %}n{% endif_greater %}{% if_greater_or_equal 1 1 %}y{% endif_greater_or_equal %}"""
        self.assertEquals(self.render(t), u'yyny')

    def test_set(self):
        t = "{% set src='import this' %}{{ src }}"
        self.assertEquals(self.render(t), u'import this')

    def test_del(self):
        t = "{% del test %}{{ test }}"
        self.assertEquals(self.render(t,{'test': 'yup'}), u'')

    def test_serialize(self):
        t = "{% serialize json users %}"
        json = self.render(t, {'users':User.objects.all()})
        self.assertEquals(deserialize('json', json).next().object.username, 'tester')

    def test_contains(self):
        t = "{% if_contains 'team' 'i' %}yup{% endif_contains %}"
        self.assertEquals(self.render(t), u'')

    def test_divisible(self):
        t = "{% if_divisible_by 150 5 %}buzz{% endif_divisible_by %}"
        self.assertEquals(self.render(t), u'buzz')

    def test_startswith(self):
        t = "{% if_startswith 'python' 'p' %}yup{% endif_startswith %}"
        self.assertEquals(self.render(t), u'yup')

    def test_subset(self):
        t = "{% if_subset l1 l2 %}yup{% endif_subset %}"
        self.assertEquals(self.render(t, {'l1':[2,3], 'l2':range(5)}), u'yup')

    def test_startswith_negate(self):
        t = "{% if_startswith 'python' 'p' negate %}yup{% endif_startswith %}"
        self.assertEquals(self.render(t), u'')

    def test_startswith_negate_else(self):
        t = "{% if_startswith 'python' 'p' negate %}yup{% else %}nope{% endif_startswith %}"
        self.assertEquals(self.render(t), u'nope')

    def test_serialize_formats(self):
        for format in ('json','python','xml'):
            t = "{% serialize format users as seria %}{{ seria|safe }}"
            seria = self.render(t, {'format':format,'users':User.objects.all()})
            if format == 'python': seria = eval(seria)
            self.assertEquals(deserialize(format, seria).next().object.username, 'tester')

    def test_setting(self):
        t = "{% if_setting 'DEBUG' %}debug{% endif_setting %}"
        self.assertEquals(self.render(t), u'debug')

    def test_sha1_filter(self):
        sha1 = '62cdb7020ff920e5aa642c3d4066950dd1f01f4d'
        self.assertEqual(self.render('{{ foo|sha1 }}', self.hash), sha1)

    def test_sha1_function(self):
        sha1 = '62cdb7020ff920e5aa642c3d4066950dd1f01f4d'
        self.assertEqual(self.render('{% sha1 foo %}', self.hash), sha1)

    def test_md5_2X(self):
        md5 = '37b51d194a7513e45b56f6524f2d51f2'
        self.assertEqual(self.render('{{ foo|md5 }}{% md5 foo %}', self.hash), md5*2)

    def test_greater(self):
        t = '{% if_greater 2 1 %}yup{% endif_greater %}'
        self.assertEquals(self.render(t), u'yup')

    def test_render_block(self):
        t = '{% render_block as myvar %}hello {{ place }}{% endrender_block %}{{ myvar }}'
        self.assertEquals(self.render(t, {'place':'world'}), 'hello world')

    def test_get_latest_object(self):
        t = '{% get_latest_object auth.user date_joined %}'
        self.assertEquals(self.render(t), 'tester')

    def test_get_latest_objects(self):
        t = '{% get_latest_objects auth.user 10 %}'
        self.assertEquals(self.render(t), '[<User: tester>]')

    def test_get_random_object(self):
        t = '{% get_random_object auth.user %}'
        self.assertEquals(self.render(t), 'tester')

    def test_get_random_objects(self):
        t = '{% get_random_objects auth.user 10 %}'
        self.assertEquals(self.render(t), '[<User: tester>]')

    def test_retrieve_object(self):
        t = '{% retrieve_object auth.user username=tester %}'
        self.assertEquals(self.render(t), 'tester')

    def test_matches(self):
        t = "{% if_matches '\w{4}' 'hiya' %}yup{% endif_matches %}"
        self.assertEquals(self.render(t), u'yup')

    def test_search(self):
        t = "{% search '^(\d{3})$' 800 as match %}{{ match.groups|safe }}"
        self.assertEquals(self.render(t), u"('800',)")

    def test_substitute(self):
        t = "{% substitute 'ROAD$' 'RD.' '100 NORTH MAIN ROAD' %}"
        self.assertEquals(self.render(t), u'100 NORTH MAIN RD.')

    def test_map(self):
        t = '{% map sha1 hello world as hashes %}{{ hashes|join:"-" }}'
        self.assertEquals(self.render(t),  u'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d-7c211433f02071597741e6ff5a8ea34789abbf43')

    def test_reduce(self):
        t = '{% reduce add 300 30 3 %}'
        self.assertEquals(self.render(t), u'333')

    def test_calendar_month(self):
        self.assert_(self.render('{% calendar month 2009 10 %}').startswith('<table'))

    def test_calendar_year(self):
        self.assert_(self.render('{% calendar year 2009 %}').startswith('<table'))

    def test_calendar_yearpage(self):
        self.assert_(self.render('{% calendar yearpage 2009 %}').startswith('<?xml version="1.0" encoding="ascii"?>'))


    def test_randrange(self):
        self.assert_(self.render('{% randrange 10 %}' in map(str,range(10))))

    def test_randint(self):
        self.assert_(0 <= int(self.render('{% randint 0 10 %}')) <= 10)

    def test_randchoice(self):
        self.assert_(self.render('{% randchoice 1 2 3 %}' in '123'))

    def test_random(self):
        self.assert_(0. <= float(self.render('{% random %}')) < 1.)

    def test_b64encode(self):
        self.assertEquals(self.render('{% b64encode "hello world" %}'), 'aGVsbG8gd29ybGQ=')

    def test_b64decode(self):
        self.assertEquals(self.render( '{% b64decode encoded %}',{'encoded':"aGVsbG8gd29ybGQ="}), 'hello world')

    try:
        import hashlib
        def test_sha224_hashlib(self):
            ctx = {'foo':'bar'}
            sha224 = u'07daf010de7f7f0d8d76a76eb8d1eb40182c8d1e7a3877a6686c9bf0'
            self.assertEquals(self.render('{{ foo|sha224 }}{% sha224 foo %}', ctx), sha224*2)
    except ImportError:
        pass

    try:
        import GChartWrapper
        def test_gchart(self):
            t = '''{% gchart bvg data encoding=text instance=true as chart %}
                scale 0 59
                color lime red blue
                legend Goucher Truman Kansas
                fill c lg 45 cccccc 0 black 1
                fill bg s cccccc
                size 200 100
                title mytittle
                axes.type x
                axes.label label2
            {% endgchart %}{{chart.checksum}}'''
            self.assertEquals(
                self.render(t, {'data':[[31],[59],[4]]}),
                '77f733ad30d44411b5b5fcac7e5848b5d5f2dd04')
    except ImportError:
        pass
    try:
        import pygments
        def test_highlight_style(self):
            t = '<style>{% highlight_style style=native cssclass=srcdiv %}</style>'
            self.assert_(self.render(t).startswith('<style>.srcdiv .hll { background-color: #404040 }'))

        def test_highlight(self):
            t = '{% highlight src python cssclass=srcdiv %}'
            self.assertEqual(self.render(t,{'src':'print "hello world"'}),
                '<div class="srcdiv"><pre><span class="k">print</span> <span class="s">&quot;hello world&quot;</span>\n</pre></div>\n')
    except ImportError:
        pass


    try:
        import feedparser
        def test_parse_feed(self):
            t = '{% load cache %}{% cache 3600 ljworld %}{% parse_feed "http://www2.ljworld.com/rss/headlines/" as ljworld_feed %}{{ ljworld_feed.keys|safe }}{% endcache %}'
            self.assertEquals(self.render(t), "['feed', 'status', 'version', 'encoding', 'bozo', 'headers', 'etag', 'href', 'namespaces', 'entries']")
    except ImportError:
        pass

    # To test this next one:
    #   get markdown (pip install markdown)
    #   add 'django.contrib.markup'  to your INSTALLED_APPS
    try:
        import markdown
        if 'django.contrib.markup' in djsettings.INSTALLED_APPS:
            def test_markdown(self):
                t = "{{ src|markdown }}"
                self.assertEquals(self.render(t, {'src':'`i`'}), u'<p><code>i</code></p>')
    except ImportError:
        pass
