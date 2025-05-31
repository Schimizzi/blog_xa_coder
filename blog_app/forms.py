from django import forms
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget # Para usar el widget de CKEditor

class PostForm(forms.ModelForm):
    """
    Formulario para crear y actualizar Posts.
    """
    # Sobrescribir los widgets para los campos de CKEditor si se quiere una configuración específica
    # o si no se está usando RichTextUploadingField directamente en el modelo, sino TextField.
    # Si ya usas RichTextUploadingField en el modelo, esto es más para personalización.
    summary = forms.CharField(
        widget=CKEditorUploadingWidget(config_name='default'), # 'default' es el nombre de la config en settings.py
        label="Resumen Corto / Introducción",
        required=False,
        help_text="Un breve resumen que aparecerá en la lista de posts."
    )
    content = forms.CharField(
        widget=CKEditorUploadingWidget(config_name='default'),
        label="Contenido Principal",
        required=True
    )

    class Meta:
        model = Post
        fields = [
            'title', 
            'slug', 
            'summary', 
            'content', 
            'featured_image', 
            'status', 
            'published_date',
            'meta_description',
            'keywords',
        ]
        # El campo 'author' se asignará automáticamente en la vista al usuario logueado.

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del Post'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se generará automáticamente si se deja vacío'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'published_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M' # Formato esperado por el widget datetime-local
            ),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción breve para SEO (máx. 160 caracteres)'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Palabras clave separadas por comas'}),
        }
        
        help_texts = {
            'slug': 'Dejar en blanco para que se genere automáticamente a partir del título. Debe ser único.',
            'featured_image': 'Opcional. Imagen principal que se mostrará para el post.',
            'published_date': 'Puedes programar la publicación para una fecha y hora futuras.',
        }
        
        labels = {
            'title': 'Título Principal del Post',
            'slug': 'Fragmento de URL (Slug)',
            'featured_image': 'Imagen Destacada',
            'status': 'Estado de Publicación',
            'published_date': 'Fecha y Hora de Publicación',
            'meta_description': 'Meta Descripción (SEO)',
            'keywords': 'Palabras Clave (SEO)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El campo 'author' no se incluye en el formulario ya que se asignará en la vista.
        # Si el slug está vacío y hay una instancia (es decir, estamos editando),
        # no queremos que se genere automáticamente de nuevo a menos que el título cambie mucho.
        # La lógica de generación de slug está en el modelo.
        # Aquí solo nos aseguramos de que si ya tiene un slug, se muestre.
        if self.instance and self.instance.pk:
            self.fields['slug'].widget.attrs['placeholder'] = self.instance.slug
        
        # Asegurar que el formato del widget de fecha sea el correcto para la entrada HTML5
        self.fields['published_date'].input_formats = ('%Y-%m-%dT%H:%M',)


    def clean_slug(self):
        """
        Asegura que el slug sea único si se proporciona manualmente.
        Si está vacío, el modelo se encargará de generarlo.
        """
        slug = self.cleaned_data.get('slug')
        if slug: # Solo validar si el usuario ingresó un slug
            # Excluir la instancia actual si estamos editando
            queryset = Post.objects.filter(slug=slug)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError("Este slug ya está en uso. Por favor, elige otro o déjalo en blanco para que se genere automáticamente.")
        return slug

