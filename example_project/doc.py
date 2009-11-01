from native_tags import register

data = {}

for k,v in register.tags:
    try:
        v = v.__module__.split('native_tags.contrib.')[1]
    except IndexError:
        continue
    if v in data:
        data[v] += (k,)
    else:
        data[v] = ()

for k,v in data.items():
    f=open('%s.rst'%k,'w')
    f.write(""".. _contrib-%s:

:mod:`%s`
====================================

.. automodule:: native_tags.contrib.%s
    
""" % (k,k,k))
    for tag in v:
        f.write("    .. autofunction:: %s\n" % tag)
    f.close()
    
