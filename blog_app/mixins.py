from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Post

class AuthorRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != request.user:
            messages.error(request, "No tienes permiso para editar o eliminar este post, ya que no eres el autor.")
            if hasattr(obj, 'get_absolute_url'):
                return redirect(obj.get_absolute_url())
            return redirect('blog:post_list') 
        
        return super().dispatch(request, *args, **kwargs)

class StaffRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect('blog:home') 
        return super().dispatch(request, *args, **kwargs)

