from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from .models import Productos
from applications.historial_precio.models import Historial_precio
# Create your views here.


class getProductoByPrice(ListView):
    template_name = "productos/getProducto.html"
    paginate_by = 20
    context_object_name = 'Productos'

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', '')
        if palabra_clave:
            lista_productos = Productos.objects.filter(
                Q(name__icontains=palabra_clave) | Q(name__iexact=palabra_clave)
            )
            resultados = []
            for producto in lista_productos:
                precio = Historial_precio.objects.filter(
                    productId=producto
                ).order_by('-date').values('price').first()
                if precio:
                    resultados.append((producto, precio['price']))
                else:
                    resultados.append((producto, None))
            resultados.sort(key=lambda x: x[1])
        else:
            resultados = []

        #print('lista resultados: ', lista_productos)
        #print('precios: ', precio)
        print('resultados', resultados)
        return resultados
