from django.template import VariableNode, TextNode
from GChartWrapper import GChart

from native_tags.decorators import block


CMDS = ('title','axes.type','axes.label','type','encoding','fill','color','scale','legend')

def parse_cmd(value):
    value = value.lstrip()
    for cmd in CMDS:
        if value.startswith(cmd):
            return cmd,value[len(cmd):].strip()
    return None, None

def gchart(context, nodelist, type, dataset, **kwargs):
    G = GChart(type, dataset, encoding=kwargs.pop('encoding','text'))
    for node in nodelist:
        if isinstance(node, TextNode):
            for part in node.render(context).splitlines():
                cmd,value = parse_cmd(part)
                if cmd is None: continue
                if cmd.startswith('axes'):
                    cmd = getattr(G.axes, cmd[5:])
                else:
                    cmd = getattr(G, cmd)
                cmd(*value.split())
    if 'instance' in kwargs:
        return G
    return G.img(**kwargs)
gchart = block(gchart)
