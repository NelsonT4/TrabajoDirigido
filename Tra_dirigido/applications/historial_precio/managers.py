from django.db import models

class Historial_Manager(models.Manager):
    def Consultar_Historial(self, kword):
        if kword:
            lista = self.filter(
                productId__name__icontains=kword,
                productId__name__iexact=kword
            ).order_by('date', 'price')
        else:
            lista = []
        #print('lista resultados: ', lista)
        return lista
    def Consultar_histori_producto(self,kword):
        lista = self.filter(
            productId__id=kword
        ).order_by('-date')
        return lista
