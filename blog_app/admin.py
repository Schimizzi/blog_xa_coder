from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Post.
    """
    list_display = ('title', 'author', 'status', 'published_date', 'created_at', 'updated_at', 'is_published')
    list_filter = ('status', 'author', 'published_date', 'created_at')
    search_fields = ('title', 'summary', 'content', 'author__username')
    
    # El campo 'slug' se puede pre-rellenar automáticamente a partir del 'title' en el admin.
    prepopulated_fields = {'slug': ('title',)}
    
    date_hierarchy = 'published_date' # Navegación por fechas en la parte superior de la lista
    ordering = ('-published_date',)
    
    # Campos que se mostrarán en el formulario de edición del admin
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'status', 'published_date')
        }),
        ('Contenido Principal', {
            'classes': ('collapse',), # Opcional: colapsar esta sección por defecto
            'fields': ('summary', 'content', 'featured_image')
        }),
        ('SEO y Metadatos (Opcional)', {
            'classes': ('collapse',),
            'fields': ('meta_description', 'keywords')
        }),
    )

    # Para mostrar campos de solo lectura (como created_at, updated_at) si se desea
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        # Optimizar consultas si es necesario
        return super().get_queryset(request).select_related('author')

