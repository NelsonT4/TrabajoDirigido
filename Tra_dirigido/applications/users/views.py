from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import (
    FormView,
    TemplateView
)
from .forms import UserRegisterForm, LoginForm
from .models import User
from django.contrib.auth import authenticate, login

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
class HomeUserView(TemplateView):
    template_name = "usuarios/index.html"

class LoginUser(FormView):
    template_name = "usuarios/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("users_app:index")
    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)
