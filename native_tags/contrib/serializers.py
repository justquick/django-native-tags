from django.core.serializers import serialize
    

serialize.function = 1

def serialize_json(queryset): return serialize('json', queryset)
serialize_json.function = 1

def serialize_xml(queryset): return serialize('xml', queryset)
serialize_xml.function = 1

def serialize_python(queryset): return serialize('python', queryset)
serialize_python.function = 1

def serialize_yaml(queryset): return serialize('yaml', queryset)
serialize_yaml.function = 1

