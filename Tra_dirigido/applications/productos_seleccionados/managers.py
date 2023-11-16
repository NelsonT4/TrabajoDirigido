from django.db import models

class ProductosSelecionaadosManager(models.Manager):
    def add_productos_selecionados(self, userId, proeductId):
        user = self.get(id=userId)
        print(userId)

