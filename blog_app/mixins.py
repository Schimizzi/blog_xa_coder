from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Post # Asumiendo que tu modelo se llama Post

class AuthorRequiredMixin(AccessMixin):
    """
    Mixin que verifica que el usuario logueado es el autor del objeto (Post).
    Se usa para vistas de edición y eliminación de posts.
    """
    def dispatch(self, request, *args, **kwargs):
        # 'self.get_object()' es un método que las DetailView, UpdateView, DeleteView tienen.
        # Para UpdateView y DeleteView, el objeto se obtiene automáticamente.
        # Si es una DetailView, necesitarías asegurarte que el objeto se carga antes de este check.
        
        # Intentamos obtener el objeto de la manera estándar de las CBV
        # Si la vista es UpdateView o DeleteView, self.object ya estará seteado
        # o self.get_object() lo cargará.
        obj = self.get_object()

        if obj.author != request.user:
            messages.error(request, "No tienes permiso para editar o eliminar este post, ya que no eres el autor.")
            # Redirigir a la página de detalle del post o a la lista de posts
            if hasattr(obj, 'get_absolute_url'):
                return redirect(obj.get_absolute_url())
            return redirect('blog:post_list') # URL de fallback
        
        return super().dispatch(request, *args, **kwargs)

class StaffRequiredMixin(AccessMixin):
    """
    Mixin que verifica que el usuario logueado es parte del staff.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect('blog:home') # O a donde consideres apropiado
        return super().dispatch(request, *args, **kwargs)

