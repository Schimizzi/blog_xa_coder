from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView, PasswordChangeView as AuthPasswordChangeView, PasswordChangeDoneView as AuthPasswordChangeDoneView
from django.contrib.auth.decorators import login_required # Decorador para vistas basadas en funciones
from django.contrib.auth.mixins import LoginRequiredMixin # Mixin para vistas basadas en clases
from django.views.generic import CreateView, DetailView, UpdateView, FormView
from django.contrib import messages # Para mostrar mensajes al usuario
from django.http import HttpResponseRedirect

from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.

class RegisterView(CreateView):
    """
    Vista para el registro de nuevos usuarios.
    Utiliza el CustomUserCreationForm.
    """
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login') # Redirige al login después de un registro exitoso

    def form_valid(self, form):
        """
        Si el formulario es válido, guarda el nuevo usuario y lo loguea.
        Luego redirige a la success_url.
        """
        user = form.save()
        # login(self.request, user) # Opcional: loguear al usuario inmediatamente después del registro
        messages.success(self.request, f"¡Cuenta creada para {user.username}! Ahora puedes iniciar sesión.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Registro de Nuevo Usuario"
        return context

class CustomLoginView(AuthLoginView):
    """
    Vista para el inicio de sesión de usuarios.
    Hereda de la vista LoginView de Django.
    """
    template_name = 'accounts/login.html'
    # success_url se define por LOGIN_REDIRECT_URL en settings.py
    # o por el parámetro 'next' en la URL.

    def form_valid(self, form):
        """
        Añade un mensaje de éxito después de un inicio de sesión válido.
        """
        messages.success(self.request, f"¡Bienvenido de nuevo, {form.get_user().username}!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Nombre de usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Iniciar Sesión"
        return context


class CustomLogoutView(LoginRequiredMixin, AuthLogoutView):
    """
    Vista para el cierre de sesión de usuarios.
    Hereda de la vista LogoutView de Django.
    Asegura que el usuario esté logueado para poder desloguearse.
    """
    # LOGOUT_REDIRECT_URL en settings.py define a dónde ir después del logout.
    # template_name = 'accounts/logout_confirm.html' # Opcional si quieres una página de confirmación
    
    def dispatch(self, request, *args, **kwargs):
        # Añadir un mensaje antes de que la lógica de logout de la superclase se ejecute
        if request.user.is_authenticated:
            messages.info(request, f"Has cerrado sesión. ¡Hasta pronto, {request.user.username}!")
        return super().dispatch(request, *args, **kwargs)


@login_required # Decorador para asegurar que solo usuarios logueados puedan ver su perfil
def profile_view(request, username=None):
    """
    Vista para mostrar el perfil de un usuario.
    Si no se proporciona username, muestra el perfil del usuario logueado.
    """
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    # El perfil se crea automáticamente gracias a las señales en models.py
    # profile = get_object_or_404(Profile, user=user) # Esto podría fallar si el perfil no existe
    profile, created = Profile.objects.get_or_create(user=user)

    context = {
        'profile_user': user, # El usuario cuyo perfil se está viendo
        'profile': profile,
        'page_title': f"Perfil de {user.username}"
    }
    return render(request, 'accounts/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para que los usuarios actualicen su perfil (User y Profile).
    Maneja dos formularios: UserUpdateForm y ProfileUpdateForm.
    """
    template_name = 'accounts/profile_form.html'
    # No se usa 'model' o 'form_class' directamente porque manejamos dos formularios.
    # success_url se define en get_success_url.

    def get_object(self, queryset=None):
        # Devuelve el usuario actual que se está editando
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        if 'profile_form' not in context:
            context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        context['page_title'] = "Editar Perfil"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # El usuario actual
        # Pasa request.POST y request.FILES a ambos formularios
        user_form = UserUpdateForm(request.POST, instance=self.request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=self.request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            # Si hay errores, vuelve a renderizar la página con los formularios y sus errores
            return self.render_to_response(
                self.get_context_data(user_form=user_form, profile_form=profile_form)
            )

    def get_success_url(self):
        # Redirige a la vista del perfil del usuario actual
        return reverse('accounts:profile_view_self')


class CustomPasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    """
    Vista para que los usuarios cambien su contraseña.
    """
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done') # Redirige a una vista de éxito

    def form_valid(self, form):
        messages.success(self.request, '¡Tu contraseña ha sido cambiada exitosamente!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Cambiar Contraseña"
        return context

class CustomPasswordChangeDoneView(LoginRequiredMixin, AuthPasswordChangeDoneView):
    """
    Vista que se muestra después de que el usuario ha cambiado su contraseña exitosamente.
    """
    template_name = 'accounts/password_change_done.html'
    # No se necesita un mensaje aquí ya que se puso en CustomPasswordChangeView

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contraseña Cambiada"
        return context

