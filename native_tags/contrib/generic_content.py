"""
Template tags which can do retrieval of content from any model.

"""

from django.db.models import get_model
from django.template import TemplateSyntaxError
from native_tags.decorators import function


def _get_model(model):
    m = get_model(*model.split('.'))
    if m is None:
        raise TemplateSyntaxError("Generic content tag got invalid model: %s" % model)
    return m

def get_latest_object(model, field=None):
    """
    Retrieves the latest object from a given model, in that model's
    default ordering, and stores it in a context variable.
    The optional field argument specifies which field to get_latest_by, otherwise the model's default is used
    
    Syntax::
    
        {% get_latest_object [app_name].[model_name] [field] as [varname] %}
    
    Example::
    
        {% get_latest_object comments.freecomment submitted_date as latest_comment %}
    
    """
    return _get_model(model)._default_manager.latest(field)
get_latest_object = function(get_latest_object)    


def get_latest_objects(model, num, field='?'):
    """
    Retrieves the latest ``num`` objects from a given model, in that
    model's default ordering, and stores them in a context variable.
    The optional field argument specifies which field to get_latest_by, otherwise the model's default is used
    
    Syntax::
    
        {% get_latest_objects [app_name].[model_name] [num] [field] as [varname] %}
    
    Example::
    
        {% get_latest_objects comments.freecomment 5 submitted_date as latest_comments %}
    
    """
    model = _get_model(model)
    if field == '?':
        field = model._meta.get_latest_by and '-%s' % model._meta.get_latest_by or field
    return model._default_manager.order_by(field)[:int(num)]
get_latest_objects = function(get_latest_objects)

def get_random_object(model):
    """
    Retrieves a random object from a given model, and stores it in a
    context variable.
    
    Syntax::
    
        {% get_random_object [app_name].[model_name] as [varname] %}
    
    Example::
    
        {% get_random_object comments.freecomment as random_comment %}
    
    """
    try:
        return _get_model(model)._default_manager.order_by('?')[0]
    except IndexError:
        return ''
get_random_object = function(get_random_object)

def get_random_objects(model, num):
    """
    Retrieves ``num`` random objects from a given model, and stores
    them in a context variable.
    
    Syntax::
    
        {% get_random_objects [app_name].[model_name] [num] as [varname] %}
    
    Example::
    
        {% get_random_objects comments.freecomment 5 as random_comments %}
    
    """
    return _get_model(model)._default_manager.order_by('?')[:int(num)]
get_random_objects = function(get_random_objects)

def retrieve_object(model, *args, **kwargs):
    """
    Retrieves a specific object from a given model by primary-key
    lookup, and stores it in a context variable.
    
    Syntax::
    
        {% retrieve_object [app_name].[model_name] [lookup kwargs] as [varname] %}
    
    Example::
    
        {% retrieve_object flatpages.flatpage pk=12 as my_flat_page %}
    
    """
    if len(args) == 1:
        kwargs.update({'pk': args[0]})
    _model = _get_model(model)
    try:
        return _model._default_manager.get(**kwargs)
    except _model.DoesNotExist:
        return ''
retrieve_object = function(retrieve_object)
