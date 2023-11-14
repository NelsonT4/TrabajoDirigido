from django.db import models

# Create your models here.
class Usuarios(models.Model):
    name = models.CharField('Nombre', max_length=20, null=False, unique=True)
    key = models.CharField('Contraseña', max_length=20, null=False, unique=True)
    intervalHistory = models.FloatField('Intervalo', max_length=10)

    class Meta:
        verbose_name = 'Usuarios'
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return (str(self.name) + '-' +
                str(self.key) + '-' +
                str(self.intervalHistory))
