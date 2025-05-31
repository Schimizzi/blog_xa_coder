from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save # Para crear perfil automáticamente
from django.dispatch import receiver # Para recibir la señal

# Create your models here.

def user_avatar_path(instance, filename):
    # El archivo se subirá a MEDIA_ROOT/avatars/user_<id>/<filename>
    # Asegúrate de que MEDIA_ROOT esté configurado en settings.py
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    """
    Modelo de Perfil de Usuario.
    Extiende el modelo User de Django para añadir campos adicionales.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # related_name permite acceder al perfil desde el usuario: user.profile
    
    # Campos solicitados:
    # username, email, password -> Ya están en el modelo User de Django.
    # nombre, apellido -> Ya están en el modelo User (first_name, last_name).
    
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True, default='avatars/default_avatar.png')
    # 'upload_to' especifica el subdirectorio dentro de MEDIA_ROOT.
    # 'default' especifica una imagen por defecto si no se sube ninguna.
    # Necesitarás crear la imagen 'default_avatar.png' en 'media/avatars/'.

    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="Biografía")
    # biografia/link/fecha de cumpleanios/etc.
    website_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Sitio Web / Link")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    
    # Campos adicionales que podrían ser útiles:
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    # Propiedad para obtener el nombre completo fácilmente
    @property
    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    # Si no se proporciona una imagen de avatar, se usa la por defecto.
    # Esta función asegura que siempre haya una URL de avatar.
    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            # Asegúrate que tienes una imagen default en /media/avatars/default_avatar.png
            # o ajusta esta ruta según tu STATIC_URL si la imagen por defecto es estática.
            from django.conf import settings
            return f"{settings.MEDIA_URL}avatars/default_avatar.png"


# Señal para crear o actualizar el perfil de usuario automáticamente cuando se crea/actualiza un User.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Cuando un objeto User es guardado, esta señal se dispara.
    Si el User fue recién creado, también se crea un Profile asociado.
    Si el User ya existía, simplemente se guarda el perfil (aunque aquí no hacemos cambios).
    """
    if created:
        Profile.objects.create(user=instance)
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Esto podría pasar si un usuario fue creado antes de implementar el Profile
        # o si la señal falló por alguna razón.
        Profile.objects.create(user=instance)
    except Exception as e:
        # Loguear el error si es necesario
        print(f"Error al guardar el perfil para {instance.username}: {e}")

