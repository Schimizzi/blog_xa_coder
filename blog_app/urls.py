from django.urls import path
from . import views

app_name = 'blog'  

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about_view, name='about'),
    path('pages/', views.PostListView.as_view(), name='post_list'),
    path('pages/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'), 
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),   
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),    
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
