import decimal

from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q


from .models import Productos
from applications.historial_precio.models import Historial_precio

from .ScrapyPages.DUno import cargarProductosD1
from .ScrapyPages.productosExito import cargarProductosExito
from .ScrapyPages.jumbo import cargarProductosJumbo



class getProductoByPrice(LoginRequiredMixin, ListView):
    template_name = "productos/getProducto.html"
    paginate_by = 20
    context_object_name = 'Productos'
    login_url = reverse_lazy('users_app:user-login')

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
                ).order_by('-date').values('price').exclude(price=None).first()
                if precio:
                    resultados.append((producto, precio['price']))
            resultados.sort(key=lambda x: x[1] if x[1] is not None else decimal.Decimal(0))

        else:
            resultados = []

        #print('lista resultados: ', lista_productos)
        #print('precios: ', precio)
        #print('resultados', resultados)
        return resultados
class SaveProducts(LoginRequiredMixin, View):
    template_inicio = "productos/getProductsByPrice.html"
    template_respuesta = "productos/ChargueResult.html"
    login_url = reverse_lazy('users_app:user-login')
    def get(self, requests):
        producto_a_buscar = requests.GET.get('kword')

        if not producto_a_buscar:
            return render(requests, self.template_inicio)
        else:
            productos_a_buscar = producto_a_buscar.split(",")

            cargarProductosExito(productos_a_buscar)

            cargarProductosD1()

            cargarProductosJumbo()

            resultado_busqueda = (f"Se guardaron exitosamente los productos de  '{producto_a_buscar} de exito"
                                  f" y todos los de D1 y jumbo'")

            return render(requests, self.template_respuesta, {'resultadoCargue': resultado_busqueda})

class BorrarDatos(LoginRequiredMixin, View):
    template_respuesta = "productos/ChargueResult.html"
    login_url = reverse_lazy('users_app:user-login')
    def get(self, requests):
        requests.GET

        Productos.objects.all().delete()
        Historial_precio.objects.all().delete()

        resultado_busqueda = f"Se borraron de manera exitosa los datos de las tablas Productos e Historial"

        return render(requests, self.template_respuesta, {'resultadoCargue': resultado_busqueda})
