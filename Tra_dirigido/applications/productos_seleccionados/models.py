from django.db import models
from applications.usuarios.models import Usuarios
from applications.productos.models import Productos

# Create your models here.
class Productos_Seleccionados(models.Model):
    userId = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    productId = models.ForeignKey(Productos, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Productos Seleccionados'
        unique_together = ('userId', 'productId')

    def __str__(self):
        return (str(self.userId) + '-' +
                str(self.productId))
