import datetime
from django.contrib.auth.models import User
from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase
from django.core.serializers import deserialize
from django.core.cache import cache

from native_tags.registry import register, AlreadyRegistered
from native_tags.nodes import get_cache_key

def render(src, ctx={}):
    return Template(src).render(Context(ctx))

class TemplateTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='tester', email='test')
        # User.objects.create(username='tester2', email='test2')
        # User.objects.create(username='tester3', email='test3')
        # User.objects.create(username='tester4', email='test4')
        self.hash = {'foo':'bar'}


    def test_less(self):
        t = """{% if_less 1 2 %}y{% endif_less %}{% if_less_or_equal 1 2 %}y{% endif_less_or_equal %}{% if_greater 2 1 %}n{% endif_greater %}{% if_greater_or_equal 1 1 %}y{% endif_greater_or_equal %}"""
        self.assertEqual(render(t), 'yyny')
    
    def test_set(self):
        t = "{% set src='import this' %}{{ src }}"
        self.assertEqual(render(t), 'import this')
    
    def test_del(self):
        t = "{% del test %}{{ test }}"
        self.assertEqual(render(t,{'test': 'yup'}), '')
    
    def _serialize(self, format):
        t = "{% serialize format users as seria %}{{ seria|safe }}"
        seria = render(t, {'format':format,'users':User.objects.all()})
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
        self.assertEqual(render(t), '')
    
    def test_divisible(self):
        t = "{% if_divisible_by 150 5 %}buzz{% endif_divisible_by %}"
        self.assertEqual(render(t), 'buzz')
    
    def test_startswith(self):
        t = "{% if_startswith 'python' 'p' %}yup{% endif_startswith %}"
        self.assertEqual(render(t), 'yup')
    
    def test_subset(self):
        t = "{% if_subset l1 l2 %}yup{% endif_subset %}"
        self.assertEqual(render(t, {'l1':[2,3], 'l2':range(5)}), 'yup')
    
    def test_superset(self):
        self.assertEqual(render("{% if_superset l1 l2 %}yup{% endif_superset %}",{'l1':range(5),'l2':[2,3]}),'yup')
    
    def test_endswith(self):
        self.assertEqual(render("{% if_endswith 'python' 'n' %}yup{% endif_endswith %}"), 'yup')
    
    def test_startswith_negate(self):
        t = "{% if_startswith 'python' 'p' negate %}yup{% endif_startswith %}"
        self.assertEqual(render(t), '')
    
    def test_startswith_negate_else(self):
        t = "{% if_startswith 'python' 'p' negate %}yup{% else %}nope{% endif_startswith %}"
        self.assertEqual(render(t), 'nope')
    
    def test_setting(self):
        t = "{% if_setting 'DEBUG' %}debug{% endif_setting %}"
        self.assertEqual(render(t), 'debug')
    
    def test_sha1_filter(self):
        sha1 = '62cdb7020ff920e5aa642c3d4066950dd1f01f4d'
        self.assertEqual(render('{{ foo|sha1 }}', self.hash), sha1)
    
    def test_sha1_function(self):
        sha1 = '62cdb7020ff920e5aa642c3d4066950dd1f01f4d'
        self.assertEqual(render('{% sha1 foo %}', self.hash), sha1)
    
    def test_md5_2X(self):
        md5 = '37b51d194a7513e45b56f6524f2d51f2'
        self.assertEqual(render('{{ foo|md5 }}{% md5 foo %}', self.hash), md5*2)
    
    def test_greater(self):
        t = '{% if_greater 2 1 %}yup{% endif_greater %}'
        self.assertEqual(render(t), 'yup')
    
    def test_render_block(self):
        t = '{% render_block as myvar %}hello {{ place }}{% endrender_block %}{{ myvar }}'
        self.assertEqual(render(t, {'place':'world'}), 'hello world')
    
    def test_get_latest_object(self):
        t = '{% get_latest_object auth.user date_joined %}'
        self.assertEqual(render(t), 'tester')
    
    def test_get_latest_objects(self):
        t = '{% get_latest_objects auth.user 10 %}'
        self.assertEqual(render(t), '[<User: tester>]')
    
    def test_get_random_object(self):
        t = '{% get_random_object auth.user %}'
        self.assertEqual(render(t), 'tester')
    
    def test_get_random_objects(self):
        t = '{% get_random_objects auth.user 10 %}'
        self.assertEqual(render(t), '[<User: tester>]')
    
    def test_retrieve_object(self):
        t = '{% retrieve_object auth.user username=tester %}'
        self.assertEqual(render(t), 'tester')
    
    def test_matches(self):
        t = "{% if_matches '\w{4}' 'hiya' %}yup{% endif_matches %}"
        self.assertEqual(render(t), 'yup')
    
    def test_search(self):
        t = "{% search '^(\d{3})$' 800 as match %}{{ match.groups|safe }}"
        self.assertEqual(render(t), u"('800',)")
    
    def test_substitute(self):
        t = "{% substitute 'ROAD$' 'RD.' '100 NORTH MAIN ROAD' %}"
        self.assertEqual(render(t), '100 NORTH MAIN RD.')
    
    def test_map(self):
        t = '{% map sha1 hello world as hashes %}{{ hashes|join:"-" }}'
        self.assertEqual(render(t),  'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d-7c211433f02071597741e6ff5a8ea34789abbf43')
    
    def test_reduce(self):
        t = '{% reduce add 300 30 3 %}'
        self.assertEqual(render(t), '333')
    
    def test_calendar_month(self):
        self.assert_(render('{% calendar month 2009 10 %}').startswith('<table'))
    
    def test_calendar_year(self):
        self.assert_(render('{% calendar year 2009 %}').startswith('<table'))
    
    def test_calendar_yearpage(self):
        self.assert_(render('{% calendar yearpage 2009 %}').startswith('<?xml version="1.0" encoding="ascii"?>'))
    
    def test_randrange(self):
        self.assert_(render('{% randrange 10 %}') in map(str,range(10)))
    
    def test_randint(self):
        self.assert_(0 <= int(render('{% randint 0 10 %}')) <= 10)
    
    def test_randchoice(self):
        self.assert_(render('{% randchoice 1 2 3 %}') in '123')
    
    def test_random(self):
        self.assert_(0. <= float(render('{% random %}')) < 1.)
    
    def test_loops_work(self):
        """
        Does looping while setting a context variable work
        """
        t = "{% for i in items %}{% add 1 i as roomba %}{{roomba}}{% endfor %}"
        o = render(t, {'items':[1,2,3]})
        self.assertEqual(o, "234")
    
    def test_b64encode(self):
        self.assertEqual(render('{% b64encode "hello world" %}'), 'aGVsbG8gd29ybGQ=')
    
    def test_b64decode(self):
        self.assertEqual(render('{% b64decode encoded %}', {'encoded':'aGVsbG8gd29ybGQ='}), 'hello world')
    
    def test_dynamic(self):
        self.assertEqual(eval(render('{% dynamic a b c d=1 e=2 %}')),
                          ['a', 'b', 'c', ('d', 1), ('e', 2)])
    
    def test_no_render(self):
        self.assertEqual(eval(render('{% no_render a b c d d=1 e=2 f=var %}', {'var':'hello'})),
                          ['a', 'b', 'c', 'd', ('d', '1'), ('e', '2'), ('f', 'var')])
    
    def test_filter_args(self):
        self.assertEqual(render('{{ var|myfilter:"baz" }}', {'var':'foobar'}), 'foobarbaz')
    
    def test_adder(self):
        self.assertEqual(render('{% load native humanize %}{% add 1000 100 as num %}{{ num|intcomma }}'), '1,100')
    
    def test_cmp_kwargs(self):
        self.assertEqual(render('{% if_cmp_kwargs foo=bar %}yup{% endif_cmp_kwargs %}'), 'yup')
    
    def test_zremove_tag(self):
        self.assert_('add' in register['function'])
        register.unregister('function', 'add')
        self.assert_(not 'add' in register['function'])
       
    def test_inclusion(self):
        self.assertEqual(render('{% myinc cheese %}'), 'im just here for the cheese')
    
    def test_map_builtins(self):
        self.assertEqual(render('{% map len l1 l2 l3 %}', {'l1':[1], 'l2':[1,2], 'l3':[1,2,3]}), '[1, 2, 3]')
    
    def test_smartypants(self):
        # this should b bombing, but i get DEBUG as False when testing despite the settings (just in testing?)
        self.assertEqual(render('{{ value|smartypants }}', {'value': 'wtf'}), 'wtf')
        
    def test_custom_if(self):
        self.assertEqual(render('{% ifsomething %}yup{% endifsomething %}'), 'yup')
    
    def test_filter_faker(self):
        self.assertRaises(TemplateSyntaxError, render, '{% sha1 "my | filter | faker" %}')
    
    def test_math(self):
        import math
        self.assertAlmostEqual(float(render('{% acos .3 %}')), 1.26610367278)
        self.assertEqual(float(render('{{ 1.5|floor }}')), 1.)
        self.assertEqual(float(render('{{ 4|sqrt }}')), 2.)
        self.assertAlmostEqual(float(render('{{ 180|radians }}')), math.pi)
    
    def test_native_debug(self):
        self.assertEqual(render('{% native_debug as debug %}{{ debug.keys|safe }}'), "['function', 'comparison', 'filter', 'block']")
        
    def test_cache(self):
        k = get_cache_key('function', 'date', (), {})
        self.assert_(cache.get(k) is None)
        self.assertEqual(render('{% date %}'), render('{% date %}'))
        self.assert_(isinstance(cache.get(k), datetime.datetime))
    
    def test_split(self):
        from native_tags.nodes import split
        a = 'fetch_user username as "author"'
        b = 'fetch_user "what the fuck" as "author"'
        self.assertEqual(split(a), ['fetch_user', 'username', 'as', 'author'])
        self.assertEqual(split(b), ['fetch_user', 'what the fuck', 'as', 'author'])
        
    def test_fail(self):
        self.assertEqual(render('{% fail %}'), 'woot')
    
    try:
        import hashlib
        def test_sha224_hashlib(self):
            ctx = {'foo':'bar'}
            sha224 = '07daf010de7f7f0d8d76a76eb8d1eb40182c8d1e7a3877a6686c9bf0'
            self.assertEqual(render('{{ foo|sha224 }}{% sha224 foo %}', ctx), sha224*2)
    except ImportError:
        pass
    
    try:
        import pygments
        def test_highlight_style(self):
            t = '<style>{% highlight_style style=native cssclass=srcdiv %}</style>'
            self.assert_(render(t).startswith('<style>.srcdiv .hll { background-color: #404040 }'))
    
        def test_highlight(self):
            t = '{% highlight src python cssclass=srcdiv %}'
            self.assertEqual(render(t,{'src':'print "hello world"'}),
                '<div class="srcdiv"><pre><span class="k">print</span> <span class="s">&quot;hello world&quot;</span>\n</pre></div>\n')
    
        def test_highlight_block(self):
            t = "{% highlight_block python as source %}import this{% endhighlight_block %}{{ source|safe }}"
            self.assertEqual(render(t),'<div class="highlight"><pre><span class="kn">import</span> <span class="nn">this</span>\n</pre></div>\n')
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
            {% endgchart %}{{ chart.checksum }}'''
            self.assertEqual(
                render(t, {'data':[[31],[59],[4]]}),
                '77f733ad30d44411b5b5fcac7e5848b5d5f2dd04')
    except ImportError:
        pass
    
    
    try:
        import feedparser
        def test_parse_feed(self):
            t = '{% load cache %}{% cache 3600 ljworld %}{% parse_feed "http://www2.ljworld.com/rss/headlines/" as ljworld_feed %}{{ ljworld_feed.keys|safe }}{% endcache %}'
            l = set(eval(render(t), {}, {}))
            self.assertEqual(len(l - set(['feed', 'status', 'version', 'encoding', 'bozo', 'headers', 'etag', 'href', 'namespaces', 'entries'])), 0)
    
        def test_include_feed(self):
            self.assertEqual(render('{% load cache %}{% cache 3600 ljworld2 %}{% include_feed "http://www2.ljworld.com/rss/headlines/" 10 feeds.html %}{% endcache %}'), '10 10')
    except ImportError:
        pass
    
    # To test this next one:
    #   get markdown (pip install markdown)
    #   add 'django.contrib.markup' to your INSTALLED_APPS
    try:
        import markdown
        def test_markdown(self):
            t = "{{ src|markdown }}"
            self.assertEqual(render(t, {'src':'`i`'}), '<p><code>i</code></p>')
    except ImportError:
        pass
    