from django.core.management.base import BaseCommand
from native_tags.registry import register

class Command(BaseCommand):
    def usage(self, exe):
        return '%s [bucket1 ...]\n\nLists registered tags for the given buckets if any' % exe
    
    def handle(self, *buckets, **kwargs):
        for bucket,items in register.items():
            if len(buckets) and not bucket in buckets:
                continue
            print bucket.title()
            items = [(x,y.__module__) for x,y in items.items()]
            items.sort(lambda x,y: cmp(x[1],y[1]))
            for name,mod in items:
                print '\t%s.%s' % (mod,name)
