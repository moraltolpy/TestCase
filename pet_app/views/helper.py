from django.http import HttpResponseNotAllowed

from pet_app.models import Pet


def delegate(request, get=None, post=None, put=None, delete=None, **kwargs):
    functions = {'get': get, 'post': post, 'put': put, 'delete': delete}
    fn = functions.get(request.method.lower())
    if not fn:
        allowed_methods = [http_method.upper() for http_method, view_func in functions.items() if view_func is not None]
        return HttpResponseNotAllowed(allowed_methods)
    return fn(request, **kwargs)


def user_pets(request):
    return [pet.dict() for pet in Pet.objects.filter(owner=request.user)] if not request.user.is_anonymous else []
