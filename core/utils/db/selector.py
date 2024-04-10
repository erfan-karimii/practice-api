from django.http import Http404
from django.db.models import Model


def get_object(id:int,class_:Model) -> object:
    try:
        instance = class_.objects.get(id=id)
    except class_.DoesNotExist:
        raise Http404
    
    return instance