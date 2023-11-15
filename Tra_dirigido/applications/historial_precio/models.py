from django.db import models
from applications.productos.models import Productos

# Create your models here.

#Manager

from .managers import Historial_Manager
class Historial_precio(models.Model):
    productId = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name="producto")
    date = models.DateField('Fecha Consulta', auto_now_add=True)
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2, null=True)
    priceUnit = models.DecimalField('Precio Unidad', max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name = 'Historial Precio'

    objects = Historial_Manager()

    def __str__(self):
        return (str(self.productId) + '-' +
                str(self.date) + '-' +
                str(self.price) + '-' +
                str(self.priceUnit))