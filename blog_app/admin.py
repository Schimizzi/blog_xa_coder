from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_date', 'created_at', 'updated_at', 'is_published')
    list_filter = ('status', 'author', 'published_date', 'created_at')
    search_fields = ('title', 'summary', 'content', 'author__username')
    
    prepopulated_fields = {'slug': ('title',)}
    
    date_hierarchy = 'published_date' 
    ordering = ('-published_date',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'status', 'published_date')
        }),
        ('Contenido Principal', {
            'classes': ('collapse',), 
            'fields': ('summary', 'content', 'featured_image')
        }),
        ('SEO y Metadatos (Opcional)', {
            'classes': ('collapse',),
            'fields': ('meta_description', 'keywords')
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')

