from data.models import Padron_electoral
from django.shortcuts import get_object_or_404
from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse

def my_decorator(func):
    @wraps(func, assigned=available_attrs(func))
    def wrap(request, *args, **kwargs):
        data = Padron_electoral.objects.get(pk=kwargs['padron_electoral_id'])
        #entry2 = get_object_or_404(Padron_electoral, pk=entry_id)
        d = request.GET.get('')
        if not d:
            return HttpResponse(status=404)
    return wrap