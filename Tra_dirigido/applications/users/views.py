from django.shortcuts import render
from django.urls import reverse_lazy, reverse

# Create your views here.
from django.views.generic import (
    FormView,
    TemplateView,
    View,
)
from .forms import UserRegisterForm, LoginForm
from .models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(FormView):
    template_name = "usuarios/register.html"
    form_class = UserRegisterForm
    success_url = '/'

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

class LogoutView(View):
    def get(self, request, *arg, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )
