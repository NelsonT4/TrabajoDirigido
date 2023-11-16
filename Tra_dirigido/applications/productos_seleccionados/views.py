from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from .models import Productos_Seleccionados, Productos
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
# Create your views here.


class IndexView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users_app:user-login')
    def post(self, request, *args, **kwargs):
        usuario = get_user_model().objects.get(pk=request.user.id)
        print(usuario)
        producto = Productos.objects.get(productId=self.kwargs['pk'])
        Productos_Seleccionados.objects.create(
            userId=usuario,
            productId=producto,
        )

        return HttpResponseRedirect(
            reverse(
                'users_app:index'
            )
        )
