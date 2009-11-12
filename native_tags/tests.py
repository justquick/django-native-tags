from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase
from django.conf import settings as djsettings
from django.core.serializers import deserialize

import atexit
import datetime
import os

from native_tags import settings, register
from native_tags.registry import AlreadyRegistered


TAG_TEMPLATE = """
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


    def render(self, src, ctx=None):
        e = None
        name = repr(self).split('testMethod=')[1].split('>')[0][5:]
        try:
            bit = Template(src).render(Context(ctx))
        except Exception, e:
            bit = ''
        TESTFILE.write(Template(TAG_TEMPLATE).render(Context({
            'name':name, 'doc':register.get_doc(name), 'src':src, 'bit':bit, 'error':e,
        })))
        return bit

    def setUp(self):
        self.test_user = User.objects.create(username='tester',email='test')
        self.hash = {'foo':'bar'}

        if not 'dynamic' in register['function']:
            register.function('dynamic', lambda *a, **kw: list(a) + sorted(kw.items()))

        def no_render(*a, **kw):
             return list(a) + sorted(kw.items())
        no_render.resolve = 0

        if not 'no_render' in register['function']:
            register.function(no_render)

        def myfilter(value, a,):# a, b, c):
            return value + a
        
        if not 'myfilter' in register['filter']:
            register.filter(myfilter)
            
        def adder(x, y):
            return x + y
            
        if not 'add' in register['function']:
            register.function('add', adder)
            
        def cmp_kwargs(**kw):
            return len(kw)

        if not 'cmp_kwargs' in register['comparison']:
            register.comparison(cmp_kwargs)
        
        def myinc(noun):
            return 'unittest.html', {'noun': noun}
        myinc.inclusion = 1
        
        if not 'myinc' in register['function']:
            register.function(myinc)
        
        self.tags = {}

    def test_less(self):
        t = """{% if_less 1 2 %}y{% endif_less %}{% if_less_or_equal 1 2 %}y{% endif_less_or_equal %}{% if_greater 2 1 %}n{% endif_greater %}{% if_greater_or_equal 1 1 %}y{% endif_greater_or_equal %}"""
        self.assertEqual(self.render(t), 'yyny')

    def test_set(self):
        t = "{% set src='import this' %}{{ src }}"
        self.assertEqual(self.render(t), 'import this')

    def test_del(self):
        t = "{% del test %}{{ test }}"
        self.assertEqual(self.render(t,{'test': 'yup'}), '')

    def _serialize(self, format):
        t = "{% serialize format users as seria %}{{ seria|safe }}"
        seria = self.render(t, {'format':format,'users':User.objects.all()})
        if format == 'python': seria = eval(seria)
        self.assertEqual(deserialize(format, seria).next().object.username, 'tester')

    def test_serialize_json(self):
        self._serialize('json')

    def test_serialize_python(self):
        self._serialize('python')

    def test_serialize_xml(self):
        self._serialize('xml')

    def test_contains(self):
        t = "{% if_contains 'team' 'i' %}yup{% endif_contains %}"
        self.assertEqual(self.render(t), '')

    def test_divisible(self):
        t = "{% if_divisible_by 150 5 %}buzz{% endif_divisible_by %}"
        self.assertEqual(self.render(t), 'buzz')

    def test_startswith(self):
        t = "{% if_startswith 'python' 'p' %}yup{% endif_startswith %}"
        self.assertEqual(self.render(t), 'yup')

    def test_subset(self):
        t = "{% if_subset l1 l2 %}yup{% endif_subset %}"
        self.assertEqual(self.render(t, {'l1':[2,3], 'l2':range(5)}), 'yup')

    def test_superset(self):
        self.assertEqual(self.render("{% if_superset l1 l2 %}yup{% endif_superset %}",{'l1':range(5),'l2':[2,3]}),'yup')

    def test_endswith(self):
        self.assertEqual(self.render("{% if_endswith 'python' 'n' %}yup{% endif_endswith %}"), 'yup')

    def test_startswith_negate(self):
        t = "{% if_startswith 'python' 'p' negate %}yup{% endif_startswith %}"
        self.assertEqual(self.render(t), '')

    def test_startswith_negate_else(self):
        t = "{% if_startswith 'python' 'p' negate %}yup{% else %}nope{% endif_startswith %}"
        self.assertEqual(self.render(t), 'nope')

    def test_setting(self):
        t = "{% if_setting 'DEBUG' %}debug{% endif_setting %}"
        self.assertEqual(self.render(t), 'debug')

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
        self.assertEqual(self.render(t), 'yup')

    def test_render_block(self):
        t = '{% render_block as myvar %}hello {{ place }}{% endrender_block %}{{ myvar }}'
        self.assertEqual(self.render(t, {'place':'world'}), 'hello world')

    def test_get_latest_object(self):
        t = '{% get_latest_object auth.user date_joined %}'
        self.assertEqual(self.render(t), 'tester')

    def test_get_latest_objects(self):
        t = '{% get_latest_objects auth.user 10 %}'
        self.assertEqual(self.render(t), '[<User: tester>]')

    def test_get_random_object(self):
        t = '{% get_random_object auth.user %}'
        self.assertEqual(self.render(t), 'tester')

    def test_get_random_objects(self):
        t = '{% get_random_objects auth.user 10 %}'
        self.assertEqual(self.render(t), '[<User: tester>]')

    def test_retrieve_object(self):
        t = '{% retrieve_object auth.user username=tester %}'
        self.assertEqual(self.render(t), 'tester')

    def test_matches(self):
        t = "{% if_matches '\w{4}' 'hiya' %}yup{% endif_matches %}"
        self.assertEqual(self.render(t), 'yup')

    def test_search(self):
        t = "{% search '^(\d{3})$' 800 as match %}{{ match.groups|safe }}"
        self.assertEqual(self.render(t), u"('800',)")

    def test_substitute(self):
        t = "{% substitute 'ROAD$' 'RD.' '100 NORTH MAIN ROAD' %}"
        self.assertEqual(self.render(t), '100 NORTH MAIN RD.')

    def test_map(self):
        t = '{% map sha1 hello world as hashes %}{{ hashes|join:"-" }}'
        self.assertEqual(self.render(t),  'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d-7c211433f02071597741e6ff5a8ea34789abbf43')

    def test_reduce(self):
        t = '{% reduce add 300 30 3 %}'
        self.assertEqual(self.render(t), '333')

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
        self.assertEqual(self.render('{% b64encode "hello world" %}'), 'aGVsbG8gd29ybGQ=')

    def test_b64decode(self):
        self.assertEqual(self.render('{% b64decode encoded %}', {'encoded':'aGVsbG8gd29ybGQ='}), 'hello world')

    def test_dynamic(self):
        self.assertEqual(eval(self.render('{% load native %}{% dynamic a b c d=1 e=2 %}')),
                          ['a', 'b', 'c', ('d', 1), ('e', 2)])

    def test_no_render(self):
        self.assertEqual(eval(self.render('{% load native %}{% no_render a b c d d=1 e=2 f=var %}', {'var':'hello'})),
                          ['a', 'b', 'c', 'd', ('d', '1'), ('e', '2'), ('f', 'var')])

    def test_filter_args(self):
        self.assertEqual(self.render('{% load native %}{{ var|myfilter:"baz" }}', {'var':'foobar'}), 'foobarbaz')

    def test_adder(self):
        self.assertEqual(self.render('{% load native humanize %}{% add 1000 100 as num %}{{ num|intcomma }}'), '1,100')

    def test_cmp_kwargs(self):
        self.assertEqual(self.render('{% load native %}{% if_cmp_kwargs foo=bar %}yup{% endif_cmp_kwargs %}'), 'yup')

    def test_zremove_tag(self):
        self.assert_('add' in register['function'])
        register.unregister('function', 'add')
        self.assert_(not 'add' in register['function'])
       
    def test_inclusion(self):
        self.assertEqual(self.render('{% load native %}{% myinc cheese %}'), 'im just here for the cheese')
    
    def test_map_builtins(self):
        self.assertEqual(self.render('{% map len l1 l2 l3 %}', {'l1':[1], 'l2':[1,2], 'l3':[1,2,3]}), '[1, 2, 3]')

    def test_smartypants(self):
        # this should b bombing, but i get DEBUG as False when testing despite the settings
        self.assertEqual(self.render('{{ value|smartypants }}', {'value': 'wtf'}), 'wtf')

    def test_include_feed(self):
        self.assertEqual(self.render('{% include_feed "http://www2.ljworld.com/rss/headlines/" feeds.html 10 %}'), '10 10')


    try:
        import hashlib
        def test_sha224_hashlib(self):
            ctx = {'foo':'bar'}
            sha224 = '07daf010de7f7f0d8d76a76eb8d1eb40182c8d1e7a3877a6686c9bf0'
            self.assertEqual(self.render('{{ foo|sha224 }}{% sha224 foo %}', ctx), sha224*2)
    except ImportError:
        pass


    if pygments:
        def test_highlight_style(self):
            t = '<style>{% highlight_style style=native cssclass=srcdiv %}</style>'
            self.assert_(self.render(t).startswith('<style>.srcdiv .hll { background-color: #404040 }'))

        def test_highlight(self):
            t = '{% highlight src python cssclass=srcdiv %}'
            self.assertEqual(self.render(t,{'src':'print "hello world"'}),
                '<div class="srcdiv"><pre><span class="k">print</span> <span class="s">&quot;hello world&quot;</span>\n</pre></div>\n')

        def test_highlight_block(self):
            t = "{% highlight_block python as source %}import this{% endhighlight_block %}{{ source|safe }}"
            self.assertEqual(self.render(t),'<div class="highlight"><pre><span class="kn">import</span> <span class="nn">this</span>\n</pre></div>\n')

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
            {% endgchart %}{{ chart.checksum }}'''
            self.assertEqual(
                self.render(t, {'data':[[31],[59],[4]]}),
                '77f733ad30d44411b5b5fcac7e5848b5d5f2dd04')
    except ImportError:
        pass


    try:
        import feedparser
        def test_parse_feed(self):
            t = '{% load cache %}{% cache 3600 ljworld %}{% parse_feed "http://www2.ljworld.com/rss/headlines/" as ljworld_feed %}{{ ljworld_feed.keys|safe }}{% endcache %}'
            self.assertEqual(self.render(t), "['feed', 'status', 'version', 'encoding', 'bozo', 'headers', 'etag', 'href', 'namespaces', 'entries']")
    except ImportError:
        pass

    # To test this next one:
    #   get markdown (pip install markdown)
    #   add 'django.contrib.markup'  to your INSTALLED_APPS
    try:
        import markdown
        def test_markdown(self):
            t = "{{ src|markdown }}"
            self.assertEqual(self.render(t, {'src':'`i`'}), '<p><code>i</code></p>')
    except ImportError:
        pass
