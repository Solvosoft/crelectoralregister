from django.http import HttpResponseNotFound
from django.http import Http404
from django.core.exceptions import PermissionDenied

def validRequest(function):
    def wrap(request, *args, **kwargs):
        if request.method == 'GET':
            v = request.GET.get('q')
            if not v:
               return HttpResponseNotFound('<h1>Argument "q" no specified. Pleae provide one. </h1>')
            else:
                return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap