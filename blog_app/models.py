from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField # Para texto enriquecido con subida de imágenes

# Create your models here.

def post_image_path(instance, filename):
    # El archivo se subirá a MEDIA_ROOT/post_images/post_<id>_<username>/<filename>
    return f'post_images/post_{instance.pk or "new"}_{instance.author.username}/{filename}'

class Post(models.Model):
    """
    Modelo para los posts o páginas del blog.
    """
    # Campos CharField (mínimo 3)
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=220, unique=True, help_text="Versión amigable para URL del título (se genera automáticamente si se deja vacío).", blank=True)
    # 'slug' es útil para URLs limpias, ej: /pages/mi-primer-post/
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="Autor")
    
    # Campos de texto enriquecido (usando ckeditor, mínimo 2)
    # Usamos RichTextUploadingField para permitir que se suban imágenes directamente desde el editor.
    summary = RichTextUploadingField(verbose_name="Resumen Corto / Introducción", help_text="Un breve resumen que aparecerá en la lista de posts.", blank=True, null=True)
    content = RichTextUploadingField(verbose_name="Contenido Principal")
    
    # Campo de imagen (1)
    featured_image = models.ImageField(
        upload_to=post_image_path, 
        verbose_name="Imagen Destacada",
        help_text="Imagen principal que se mostrará para el post.",
        null=True, blank=True
    )
    
    # Campos de fecha (mínimo 2)
    published_date = models.DateTimeField(verbose_name="Fecha de Publicación", default=timezone.now, help_text="Puede ser una fecha futura para programar la publicación.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    # Otros campos útiles
    STATUS_CHOICES = (
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    
    # Campos adicionales solicitados indirectamente (para el "Acerca de Mí" y otros)
    meta_description = models.CharField(max_length=160, blank=True, null=True, verbose_name="Meta Descripción (SEO)", help_text="Descripción breve para motores de búsqueda (máx. 160 caracteres).")
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name="Palabras Clave (SEO)", help_text="Palabras clave separadas por comas.")


    class Meta:
        ordering = ['-published_date'] # Ordenar los posts por fecha de publicación descendente por defecto
        verbose_name = "Post / Página"
        verbose_name_plural = "Posts / Páginas"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Devuelve la URL canónica para una instancia del post.
        Se usará para el enlace "Leer más" y en el sitemap si lo creas.
        Asume que tienes una URL llamada 'post_detail' en tu blog_app.urls que toma un slug.
        """
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar automáticamente el slug si está vacío.
        """
        if not self.slug:
            from django.utils.text import slugify
            # Genera un slug único añadiendo un contador si es necesario
            original_slug = slugify(self.title)
            queryset = Post.objects.filter(slug__iexact=original_slug).exclude(pk=self.pk)
            num = 1
            slug = original_slug
            while queryset.exists():
                slug = f"{original_slug}-{num}"
                queryset = Post.objects.filter(slug__iexact=slug).exclude(pk=self.pk)
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        """
        Propiedad para verificar si el post está publicado y la fecha de publicación no es futura.
        """
        return self.status == 'published' and self.published_date <= timezone.now()

    @property
    def get_featured_image_url(self):
        if self.featured_image and hasattr(self.featured_image, 'url'):
            return self.featured_image.url
        # Puedes retornar una imagen placeholder si no hay imagen destacada
        # from django.conf import settings
        # return f"{settings.STATIC_URL}images/default_post_image.png" # Necesitarías esta imagen
        return None # O simplemente no retornar nada

