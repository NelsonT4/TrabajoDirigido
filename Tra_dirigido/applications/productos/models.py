from django.db import models

# Create your models here.



class Productos(models.Model):
    productId = models.IntegerField('Id', primary_key=True,auto_created=False )
    store = models.CharField('Almacen', max_length=20)
    name = models.CharField('Nombre', max_length=100)
    category = models.CharField('Categoria', max_length=100)
    make = models.CharField('marca', max_length=20)
    describe = models.CharField('Descripción', max_length=100, null=True)
    basicNeed = models.BooleanField('Nececidad Basica', max_length=1, null=True)

    class Meta:
        verbose_name = 'Productos'
        verbose_name_plural = "Productos"
        unique_together = ('productId', 'store')

    def __str__(self):
        return (str(self.productId) + '-' +
                str(self.store) + '-' +
                str(self.name) + '-' +
                str(self.category) + '-' +
                str(self.make) + '-' +
                str(self.describe) + '-' +
                str(self.basicNeed))
