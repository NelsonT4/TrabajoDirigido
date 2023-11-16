from django.contrib.auth import authenticate
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic  import FormView
from .models import Productos_Seleccionados
# Create your views here.


class IndexView(FormView):
    template_name = "productos_seleccionados/productos_seleccionados.html"
    paginate_by = 20
    context_object_name = 'ProductosSelecionados'
    def form_valid(self):
        productId = self.kwargs['id']
        print(productId)
        """usuario = self.request.user
        print(usuario)
        user = authenticate(
            username=usuario.id,
        )
        producto_seeccionado = []
        if user:
            producto_seeccionado = Productos_Seleccionados(
                userId=usuario.id,
                productId=productId,
            )
            producto_seeccionado.save()"""
        return []






