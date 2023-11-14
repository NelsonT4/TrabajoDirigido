from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from .models import Historial_precio
# Create your views here.

class ListaHistorialPrecio(ListView):
     template_name = 'historial_precio/historial_precio.html'
     paginate_by = 5
     ordering = '-date', 'price'
     context_object_name = 'Historial'

     def get_queryset(self):
          print('***')
          palabra_clave = self.request.GET.get('kword', '')
          if palabra_clave:
               lista = Historial_precio.objects.filter(
                    Q(productId__name__icontains=palabra_clave) | Q(productId__name__iexact=palabra_clave)
               )
          else:
               lista=[]
          print('lista resultados: ', lista)
          return lista

class ListaHistorial(ListView):
     template_name = 'historial_precio/historial.html'
     paginate_by = 5
     ordering = '-date', 'price'
     context_object_name = 'Historia'

     def get_queryset(self):
          productId =self.kwargs['id']
          lista = Historial_precio.objects.filter(
               productId__id=productId
          ).order_by('-date')
          return lista

