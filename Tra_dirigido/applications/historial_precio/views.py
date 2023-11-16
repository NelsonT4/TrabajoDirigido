from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from .models import Historial_precio
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ListaHistorialPrecio(LoginRequiredMixin, ListView):
     template_name = 'historial_precio/historial_precio.html'
     paginate_by = 5
     ordering = '-date', 'price'
     context_object_name = 'Historial'
     login_url = reverse_lazy('users_app:user-login')

     def get_queryset(self):
          print('***')
          palabra_clave = self.request.GET.get('kword', '')
          return Historial_precio.objects.Consultar_Historial(palabra_clave)

class ListaHistorial(LoginRequiredMixin, ListView):
     template_name = 'historial_precio/historial.html'
     paginate_by = 5
     ordering = '-date', 'price'
     context_object_name = 'Historia'
     login_url = reverse_lazy('users_app:user-login')

     def get_queryset(self):
          productId =self.kwargs['id']
          return Historial_precio.objects.Consultar_histori_producto(productId)
