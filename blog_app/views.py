from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator 
from django.utils import timezone
from django.db.models import Q 
from django.contrib import messages
from django.http import Http404
from .models import Post
from .forms import PostForm
from .mixins import AuthorRequiredMixin, StaffRequiredMixin


class HomeView(TemplateView):
    template_name = 'blog_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Bienvenido al Blog!"
        context['recent_posts'] = Post.objects.filter(
            status='published', 
            published_date__lte=timezone.now()
        ).order_by('-published_date')[:5]
        return context

def about_view(request):
    context = {
        'owner_name': "Soy Claudio Schimizzi", 
        'owner_bio': "Un entusiasta de la ciberseguridad con una habilidad especial para desarrollar scripts en Python, buscando constantemente automatizar procesos y crear herramientas para la detección y análisis de amenazas.",
        'owner_image_url': "https://placehold.co/300x300/007bff/white?text=Dueño"
    }
    return render(request, 'blog_app/about.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog_app/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5 

    def get_queryset(self):
        queryset = Post.objects.filter(status='published', published_date__lte=timezone.now()).order_by('-published_date')
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(summary__icontains=query) | 
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            ).distinct() 
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "El Blog del Programador"
        search_query = self.request.GET.get('q', '')
        context['search_query'] = search_query
        if search_query and not context['posts']: 
            messages.warning(self.request, f"No se encontraron posts que coincidan con '{search_query}'.")
        elif not search_query and not context['posts']: 
             messages.info(self.request, "Aún no hay posts publicados en el blog.")
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug' 
    slug_url_kwarg = 'slug' 

    def get_queryset(self):
        qs = super().get_queryset().filter(published_date__lte=timezone.now())
        if self.request.user.is_authenticated:
            qs = qs | Post.objects.filter(
                Q(slug=self.kwargs['slug']) & 
                (Q(author=self.request.user) | Q(author__is_staff=True))
            )
            return qs.distinct()
        return qs.filter(status='published')


    def get_object(self, queryset=None):
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
    model = Post
    form_class = PostForm
    template_name = 'blog_app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "¡Post creado exitosamente!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Crear Nuevo Post"
        context['form_mode'] = "create"
        return context


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
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
    model = Post
    template_name = 'blog_app/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list') 
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, f"El post '{self.object.title}' ha sido eliminado exitosamente.")
        return response
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Confirmar Eliminación: {self.object.title}"
        return context
