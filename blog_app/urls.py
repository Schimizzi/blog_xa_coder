from django.urls import path
from . import views

app_name = 'blog'  # Namespace para las URLs de esta aplicación

urlpatterns = [
    # URL para la página de inicio
    path('', views.HomeView.as_view(), name='home'),
    
    # URL para la página "Acerca de Mí"
    path('about/', views.about_view, name='about'),
    
    # URLs para los Posts (Páginas del blog)
    # Lista de posts (la ruta "pages/" que mencionaste)
    path('pages/', views.PostListView.as_view(), name='post_list'),
    
    # Detalle de un post (se accede por slug)
    path('pages/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Crear un nuevo post
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    
    # Actualizar un post existente
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    
    # Eliminar un post existente
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
