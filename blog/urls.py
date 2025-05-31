"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog_app.urls', namespace='blog')), # URLs de la aplicación principal del blog
    path('accounts/', include('accounts.urls', namespace='accounts')), # URLs de la aplicación de cuentas
    
    # URL para CKEditor (subida de imágenes)
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Servir archivos de media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Handler para error 404 personalizado (opcional, si creas templates/404.html)
# from django.conf.urls import handler404
# handler404 = 'blog_app.views.custom_404_view' # Necesitarías crear esta vista
