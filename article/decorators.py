from django.contrib import messages
from django.shortcuts import redirect,get_object_or_404
from .models import Article


def user_is_entry_author(function):   #checking if the logged in user is the owner of the entry.
    def wrap(request, *args, **kwargs):
        entry = get_object_or_404(Article,pk=kwargs['id'])
        if entry.author == request.user:
            return function(request, *args, **kwargs)
        else:
            messages.warning(request,"Böyle bir makale yok veya bu işleme yetkiniz yok")
            return redirect("index") 
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap