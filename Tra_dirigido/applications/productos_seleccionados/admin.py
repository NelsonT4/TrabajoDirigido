from django.contrib import admin
from .models import Productos_Seleccionados

# Register your models here.

class ProductosSeleccionadosAdmin(admin.ModelAdmin):
    list_display = (
        'userId',
        'productId',
    )

admin.site.register(Productos_Seleccionados, ProductosSeleccionadosAdmin)