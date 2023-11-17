from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView
from .models import Productos_Seleccionados, Productos
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
# Create your views here.


class IndexView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users_app:user-login')
    def post(self, request, *args, **kwargs):
        usuario = get_user_model().objects.get(pk=request.user.id)
        producto, created = Productos.objects.get_or_create(productId=self.kwargs['pk'])

        productos_seleccionados_exists = Productos_Seleccionados.objects.filter(
            userId=usuario,
            productId=producto,
        ).exists()

        if not productos_seleccionados_exists:
            Productos_Seleccionados.objects.create(
                userId=usuario,
                productId=producto,
            )
        return HttpResponseRedirect(
            reverse('productosSeleccionado_app:favoritos')
        )
class ConsultarFavoritos(LoginRequiredMixin, ListView):

    template_name = 'productos_seleccionados/productos_seleccionados.html'
    paginate_by = 4
    context_object_name = 'Favoritos'
    login_url = reverse_lazy('users_app:user-login')
    def get_queryset(self):
        return Productos_Seleccionados.objects.ConsultarFavoritos(self.request.user)
class EliminarFavorito(LoginRequiredMixin, DeleteView):
    model = Productos_Seleccionados
    success_url = reverse_lazy('productosSeleccionado_app:favoritos')