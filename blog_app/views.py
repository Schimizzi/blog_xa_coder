from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin # Para CBV que requieren login
from django.contrib.auth.decorators import login_required # Para FBV que requieren login
from django.utils.decorators import method_decorator # Para usar decoradores en métodos de CBV
from django.utils import timezone
from django.db.models import Q # Para búsquedas complejas (OR)
from django.contrib import messages
from django.http import Http404


from .models import Post
from .forms import PostForm
from .mixins import AuthorRequiredMixin, StaffRequiredMixin # Importamos nuestro mixin

# Create your views here.

class HomeView(TemplateView):
    """
    Vista para la página de inicio.
    Podría mostrar los posts más recientes o contenido destacado.
    """
    template_name = 'blog_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Bienvenido a Mi Blog Personal"
        # Mostrar algunos posts recientes en la home
        context['recent_posts'] = Post.objects.filter(
            status='published', 
            published_date__lte=timezone.now()
        ).order_by('-published_date')[:5] # Los 5 más recientes
        return context

# Vista "Acerca de Mí" - Usaremos una vista basada en función para aplicar un decorador simple
# como ejemplo, aunque podría ser una TemplateView.
# @login_required # Ejemplo de decorador, si esta página requiriera login
def about_view(request):
    """
    Vista para la página "Acerca de Mí".
    El contenido puede ser estático en la plantilla o cargado desde la DB si se prefiere.
    """
    # Si quisieras cargar el contenido desde un Post específico (ej. un post del admin):
    # try:
    #     about_post = Post.objects.get(slug='acerca-de-mi-pagina', status='published')
    # except Post.DoesNotExist:
    #     about_post = None
    # context = {'page_title': "Acerca de Mí", 'about_post': about_post}
    
    context = {
        'page_title': "Acerca de Mí",
        # Puedes pasar más contexto aquí si es necesario
        'owner_name': "El Dueño del Blog", # Ejemplo
        'owner_bio': "Aquí va una breve descripción sobre el dueño del blog, sus pasiones, y lo que los lectores pueden esperar encontrar aquí. Este contenido puede ser editado directamente en la plantilla o, para mayor flexibilidad, podría cargarse desde un objeto 'AboutPage' en la base de datos o un post específico.",
        'owner_image_url': "https://placehold.co/300x300/007bff/white?text=Dueño" # URL de ejemplo
    }
    return render(request, 'blog_app/about.html', context)


class PostListView(ListView):
    """
    Vista para listar todos los posts publicados (páginas del blog).
    Maneja la ruta "pages/".
    También incluye funcionalidad de búsqueda.
    """
    model = Post
    template_name = 'blog_app/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5 # Muestra 5 posts por página

    def get_queryset(self):
        queryset = Post.objects.filter(status='published', published_date__lte=timezone.now()).order_by('-published_date')
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(summary__icontains=query) | 
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            ).distinct() # distinct() para evitar duplicados si un término aparece en múltiples campos
        
        # No es necesario un 404 si no hay posts, ListView maneja 'object_list' vacío.
        # El mensaje "No hay posts" se maneja en la plantilla.
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Todas las Páginas del Blog"
        search_query = self.request.GET.get('q', '')
        context['search_query'] = search_query
        if search_query and not context['posts']: # Si hubo búsqueda y no hay resultados
            messages.warning(self.request, f"No se encontraron posts que coincidan con '{search_query}'.")
        elif not search_query and not context['posts']: # Si no hubo búsqueda y no hay posts en general
             messages.info(self.request, "Aún no hay posts publicados en el blog.")
        return context


class PostDetailView(DetailView):
    """
    Vista para mostrar el detalle de un post específico.
    Se accede mediante el slug del post en la URL (ej. "pages/<slug>/").
    """
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug' # Campo en el modelo Post a usar para la búsqueda por slug
    slug_url_kwarg = 'slug' # Nombre del argumento de la URL que contiene el slug

    def get_queryset(self):
        # Solo mostrar posts publicados, a menos que el usuario sea el autor o staff
        qs = super().get_queryset().filter(published_date__lte=timezone.now())
        if self.request.user.is_authenticated:
            # Permitir ver posts en borrador si eres el autor o staff
            qs = qs | Post.objects.filter(
                Q(slug=self.kwargs['slug']) & 
                (Q(author=self.request.user) | Q(author__is_staff=True))
            )
            return qs.distinct()
        return qs.filter(status='published')


    def get_object(self, queryset=None):
        """
        Sobrescribimos get_object para manejar el caso de que el post no exista o no esté publicado.
        El user story dice: "Si no existe ninguna página mostrar un "Oooops! 404 Error!"."
        DetailView ya lanza un Http404 si no encuentra el objeto con el slug dado.
        Aquí nos aseguramos que también se lance si el post no está publicado (para usuarios no autores/staff).
        """
        obj = super().get_object(queryset)
        if not obj.is_published and not (self.request.user.is_authenticated and (self.request.user == obj.author or self.request.user.is_staff)):
            raise Http404("El post que buscas no está disponible o no existe.")
        return obj


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context.get('post')
        if post:
            context['page_title'] = post.title
            context['meta_description'] = post.meta_description or post.summary[:160]
            context['meta_keywords'] = post.keywords
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear un nuevo post.
    Requiere que el usuario esté logueado (LoginRequiredMixin).
    """
    model = Post
    form_class = PostForm
    template_name = 'blog_app/post_form.html'
    # success_url se define en get_success_url o directamente aquí si es fijo.

    def form_valid(self, form):
        """
        Asigna el usuario logueado como autor del post antes de guardarlo.
        """
        form.instance.author = self.request.user
        messages.success(self.request, "¡Post creado exitosamente!")
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige al detalle del post recién creado
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Crear Nuevo Post"
        context['form_mode'] = "create"
        return context


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """
    Vista para actualizar un post existente.
    Requiere que el usuario esté logueado (LoginRequiredMixin).
    Requiere que el usuario sea el autor del post (AuthorRequiredMixin).
    """
    model = Post
    form_class = PostForm
    template_name = 'blog_app/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, "¡Post actualizado exitosamente!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Editando Post: {self.object.title}"
        context['form_mode'] = "update"
        return context


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """
    Vista para eliminar un post existente.
    Requiere que el usuario esté logueado (LoginRequiredMixin).
    Requiere que el usuario sea el autor del post (AuthorRequiredMixin).
    """
    model = Post
    template_name = 'blog_app/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list') # Redirige a la lista de posts después de eliminar
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def post(self, request, *args, **kwargs):
        # Sobrescribimos post para añadir un mensaje de éxito.
        # La lógica de eliminación la maneja la superclase.
        # Es importante llamar a super().post() para que realmente se elimine.
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, f"El post '{self.object.title}' ha sido eliminado exitosamente.")
        return response
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Confirmar Eliminación: {self.object.title}"
        return context

# Vista para el error 404 personalizado (opcional)
# def custom_404_view(request, exception):
#    return render(request, '404.html', {}, status=404)
