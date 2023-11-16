from django.db import models
from django.db.models import Q


class Historial_Manager(models.Manager):
    def Consultar_Historial(self, kword):
        if kword:
            lista = self.filter(
                Q(productId__name__icontains=kword) | Q(productId__name__iexact=kword)
            ).order_by('date', 'price').exclude(price=None)
        else:
            lista = []
        print('lista resultados: ', lista)
        return lista
    def Consultar_histori_producto(self,kword):
        lista = self.filter(
            productId__productId=kword
        ).order_by('-date')
        return lista
