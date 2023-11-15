import decimal

from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.shortcuts import render

from django.db.models import Q
from .models import Productos
from applications.historial_precio.models import Historial_precio

from .ScrapyPages.DUno import cargarProductosD1
from .ScrapyPages.productosExito import cargarProductosExito
from .ScrapyPages.jumbo import cargarProductosJumbo

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
            resultados.sort(key=lambda x: x[1] if x[1] is not None else decimal.Decimal(0))

        else:
            resultados = []

        #print('lista resultados: ', lista_productos)
        #print('precios: ', precio)
        print('resultados', resultados)
        return resultados
class SaveProducts(View):
    template_inicio = "productos/getProductsByPrice.html"
    template_respuesta = "productos/viewCompareProducts.html"

    def get (self, requests):
        producto_a_buscar = requests.GET.get('kword')

        if not producto_a_buscar:
            return render(requests, self.template_inicio)
        else:
            productos_a_buscar = producto_a_buscar.split(",")

            cargarProductosExito(productos_a_buscar)
            #
            cargarProductosD1()

            #cargarProductosJumbo()



            resultado_busqueda = f"Se guardaron exitosamente los productos de  '{producto_a_buscar}'"


            return render(requests, self.template_respuesta)