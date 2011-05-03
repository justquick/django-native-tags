from django.test import TestCase
from native_tags.registry import register


def tester(f):
    def inner(unit):
        args, kwargs = f.test.get('args', ()), f.test.get('kwargs', {})
        result = len(kwargs) and f(*args, **kwargs) or f(*args)
        unit.assertEquals(result, f.test.get('result', True))
    return inner

attrs = {}

for bucket,items in register.items():
    for name,func in items.items():
        if hasattr(func, 'test'):
            attrs['test_%s' % name] = tester(func)

NativeTagTests = type('NativeTagTests', (TestCase,), attrs)
       