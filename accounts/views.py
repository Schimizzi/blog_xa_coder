from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView, PasswordChangeView as AuthPasswordChangeView, PasswordChangeDoneView as AuthPasswordChangeDoneView
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, FormView
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.utils import timezone 
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from .models import Profile
from django.contrib.auth.models import User
from blog_app.models import Post 


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"¡Cuenta creada para {user.username}! Ahora puedes iniciar sesión.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Registro de Nuevo Usuario"
        return context

class CustomLoginView(AuthLoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
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
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, f"Has cerrado sesión. ¡Hasta pronto, {request.user.username}!")
        return super().dispatch(request, *args, **kwargs)


@login_required 
def profile_view(request, username=None):

    if username:
        profile_user = get_object_or_404(User, username=username)
        user_posts = Post.objects.filter(
            author=profile_user, 
            status='published',
            published_date__lte=timezone.now()
        ).order_by('-published_date')
    else:
        profile_user = request.user
        user_posts = Post.objects.filter(author=profile_user).order_by('-published_date')
    
    
    profile, created = Profile.objects.get_or_create(user=profile_user)

    context = {
        'profile_user': profile_user, 
        'profile': profile,
        'user_posts': user_posts, 
        'page_title': f"Perfil de {profile_user.username}"
    }
    return render(request, 'accounts/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para que los usuarios actualicen su perfil (User y Profile).
    Maneja dos formularios: UserUpdateForm y ProfileUpdateForm.
    """
    model = User 
    form_class = UserUpdateForm  
    template_name = 'accounts/profile_form.html'


    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'user_form' not in context: 
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        else:
            context['user_form'] = context.pop('form', UserUpdateForm(instance=self.request.user))


        if 'profile_form' not in context:
            context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        
        context['page_title'] = "Editar Perfil"
        return context

    def post(self, request, *args, **kwargs):
 
        self.object = self.get_object() 
        

        user_form = UserUpdateForm(request.POST, instance=self.request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=self.request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            return self.render_to_response(
                self.get_context_data(user_form=user_form, profile_form=profile_form)
            )

    def get_success_url(self):
        return reverse('accounts:profile_view_self')


class CustomPasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

    def form_valid(self, form):
        messages.success(self.request, '¡Tu contraseña ha sido cambiada exitosamente!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Cambiar Contraseña"
        return context

class CustomPasswordChangeDoneView(LoginRequiredMixin, AuthPasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contraseña Cambiada"
        return context
