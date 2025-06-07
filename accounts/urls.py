from django.urls import path
from . import views

app_name = 'accounts' 
urlpatterns = [

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_update'),
    

    path('profile/', views.profile_view, name='profile_view_self'),
    
    path('profile/<str:username>/', views.profile_view, name='profile_view_user'),

    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    
]
