from django.shortcuts import render
from django.views.generic import ListView
from pip._internal.network.session import user_agent

from applications.productos_seleccionados.models import Productos_Seleccionados
from applications.productos.models import Productos
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    FormView,
    TemplateView,
    View,
)
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm
)
from .models import User



# Create your views here.

class HomeIndex(TemplateView):
    template_name = "inicio.html"

class UserRegisterView(FormView):
    template_name = "usuarios/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users_app:index")

    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
        )

        return super(UserRegisterView, self).form_valid(form)
class HomeUserView(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/index.html"
    login_url = reverse_lazy('users_app:user-login')

class LoginUser(FormView):
    template_name = "usuarios/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("users_app:index")
    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):
    def get(self, request, *arg, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UpdatePasswordView(FormView):
    template_name = 'usuarios/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy("users_app:user-login")
    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )
        if user:
            newPassword = form.cleaned_data['password2']
            usuario.set_password(newPassword)
            usuario.save()
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)










