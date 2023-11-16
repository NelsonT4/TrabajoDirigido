from django.db import models
from applications.users.models import User
from applications.productos.models import Productos


# Create your models here.
class Productos_Seleccionados(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, )
    productId = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='products_user')

    class Meta:
        verbose_name = 'Productos Seleccionados'
        unique_together = ('userId', 'productId')


    def __str__(self):
        return (str(self.userId) + '-' +
                str(self.productId))
