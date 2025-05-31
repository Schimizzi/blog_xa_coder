from django.urls import path
from . import views

app_name = 'accounts'  # Namespace para las URLs de esta aplicación

urlpatterns = [
    # URLs de Autenticación
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # URLs de Perfil
    # La URL para editar el perfil DEBE ir ANTES de la que captura <username>
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_update'),
    
    # Vista del perfil propio (sin username en la URL, usa el usuario logueado)
    path('profile/', views.profile_view, name='profile_view_self'),
    
    # Vista del perfil de otro usuario (con username en la URL)
    # Esta es la ruta que estaba capturando 'edit' incorrectamente.
    path('profile/<str:username>/', views.profile_view, name='profile_view_user'),

    # URLs de Cambio de Contraseña
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    
    # Django también provee URLs para reseteo de contraseña, pero no las incluimos aquí por simplicidad.
    # Si las necesitas, serían algo como:
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
