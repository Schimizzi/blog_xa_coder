from django import forms
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget 

class PostForm(forms.ModelForm):
    summary = forms.CharField(
        widget=CKEditorUploadingWidget(config_name='default'), 
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

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del Post'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se generará automáticamente si se deja vacío'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'published_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'

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
        if self.instance and self.instance.pk:
            self.fields['slug'].widget.attrs['placeholder'] = self.instance.slug
        
        self.fields['published_date'].input_formats = ('%Y-%m-%dT%H:%M',)


    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug: 
            queryset = Post.objects.filter(slug=slug)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError("Este slug ya está en uso. Por favor, elige otro o déjalo en blanco para que se genere automáticamente.")
        return slug

