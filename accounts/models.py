from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver 


def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True, default='avatars/default_avatar.png')


    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="Biografía")
    website_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Sitio Web / Link")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    

    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    @property
    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    

    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            from django.conf import settings
            return f"{settings.MEDIA_URL}avatars/default_avatar.png"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
    except Exception as e:
        print(f"Error al guardar el perfil para {instance.username}: {e}")

