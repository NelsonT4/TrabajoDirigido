from django.db import models

class ProductosSelecionaadosManager(models.Manager):
    def ConsultarFavoritos(self, user):
        return self.filter(
            userId=user,
        )
