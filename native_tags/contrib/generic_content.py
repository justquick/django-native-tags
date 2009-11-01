"""
Template tags which can do retrieval of content from any model.

"""

from django.db.models import get_model

from native_tags.decorators import function


def _get_model(model): return get_model(*model.split('.'))

def get_latest_object(model, field=None):
    """
    Retrieves the latest object from a given model, in that model's
    default ordering, and stores it in a context variable.
    
    Syntax::
    
        {% get_latest_object [app_name].[model_name] as [varname] %}
    
    Example::
    
        {% get_latest_object comments.freecomment as latest_comment %}
    
    """
    return _get_model(model)._default_manager.latest(field)
get_latest_object = function(get_latest_object)    


def get_latest_objects(model, num):
    """
    Retrieves the latest ``num`` objects from a given model, in that
    model's default ordering, and stores them in a context variable.
    
    Syntax::
    
        {% get_latest_objects [app_name].[model_name] [num] as [varname] %}
    
    Example::
    
        {% get_latest_objects comments.freecomment 5 as latest_comments %}
    
    """
    return _get_model(model)._default_manager.all()[:int(num)]
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

def retrieve_object(model, **kwargs):
    """
    Retrieves a specific object from a given model by primary-key
    lookup, and stores it in a context variable.
    
    Syntax::
    
        {% retrieve_object [app_name].[model_name] [pk] as [varname] %}
    
    Example::
    
        {% retrieve_object flatpages.flatpage 12 as my_flat_page %}
    
    """
    model = _get_model(model)
    try:
        return model._default_manager.get(**kwargs)
    except model.DoesNotExist:
        return ''
retrieve_object = function(retrieve_object)
