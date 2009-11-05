#!/usr/bin/env python

import unicodedata
import re
import os
import conf


TARGETS = ('static','sources')

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

def converter(adir='./build/html'):
    for f in os.listdir(adir):
        f = os.path.join(adir, f)
        if os.path.isfile(f) and f.endswith('.html'):
            for x in TARGETS:
                os.system('sed "s/_%s/sphinx_%s/g" "%s" > "%s.tmp"' % (x,x,f,f))
                os.system('mv "%s.tmp" "%s"' % (f,f))
        elif os.path.isdir(f):
            converter(f)
            
converter()

for x in TARGETS:
    os.system('mv ./build/html/_%s ./build/html/sphinx_%s' % (x,x))

os.system('mv ./build/html %s' % slugify(conf.project))
