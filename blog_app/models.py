from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField



def post_image_path(instance, filename):
    return f'post_images/post_{instance.pk or "new"}_{instance.author.username}/{filename}'

class Post(models.Model):  
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=220, unique=True, help_text="Versión amigable para URL del título (se genera automáticamente si se deja vacío).", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="Autor")
    summary = RichTextUploadingField(verbose_name="Resumen Corto / Introducción", help_text="Un breve resumen que aparecerá en la lista de posts.", blank=True, null=True)
    content = RichTextUploadingField(verbose_name="Contenido Principal")
    
    featured_image = models.ImageField(
        upload_to=post_image_path, 
        verbose_name="Imagen Destacada",
        help_text="Imagen principal que se mostrará para el post.",
        null=True, blank=True
    )
    
    published_date = models.DateTimeField(verbose_name="Fecha de Publicación", default=timezone.now, help_text="Puede ser una fecha futura para programar la publicación.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    STATUS_CHOICES = (
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    
    meta_description = models.CharField(max_length=160, blank=True, null=True, verbose_name="Meta Descripción (SEO)", help_text="Descripción breve para motores de búsqueda (máx. 160 caracteres).")
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name="Palabras Clave (SEO)", help_text="Palabras clave separadas por comas.")


    class Meta:
        ordering = ['-published_date'] 
        verbose_name = "Post / Página"
        verbose_name_plural = "Posts / Páginas"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
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
        return self.status == 'published' and self.published_date <= timezone.now()

    @property
    def get_featured_image_url(self):
        if self.featured_image and hasattr(self.featured_image, 'url'):
            return self.featured_image.url
        return None 

