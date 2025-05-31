from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Profile.
    """
    list_display = ('user', 'full_name', 'birth_date', 'location', 'updated_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    list_filter = ('birth_date', 'updated_at')
    
    # Para mostrar campos del User directamente en el Profile admin (opcional)
    # Esto requiere un poco más de configuración si se quieren hacer editables.
    # readonly_fields = ('user_link',)

    # def user_link(self, obj):
    #     from django.urls import reverse
    #     from django.utils.html import format_html
    #     url = reverse("admin:auth_user_change", args=[obj.user.id])
    #     return format_html('<a href="{}">{}</a>', url, obj.user.username)
    # user_link.short_description = 'User'

# También podrías querer un admin inline para editar el Profile desde el User admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User

# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'

# class CustomUserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline,)
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_profile_birth_date')
#     list_select_related = ('profile',) # Optimiza la consulta

#     def get_profile_birth_date(self, instance):
#         return instance.profile.birth_date
#     get_profile_birth_date.short_description = 'Birth Date (Profile)'


# admin.site.unregister(User) # Desregistrar el User admin por defecto
# admin.site.register(User, CustomUserAdmin) # Registrar el User admin personalizado
