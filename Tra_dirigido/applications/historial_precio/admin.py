from django.contrib import admin
from .models import Historial_precio

# Register your models here.

class HistorialAdmin(admin.ModelAdmin):
    list_display = (
        'productId',
        'date',
        'price',
        'priceUnit',
    )

admin.site.register(Historial_precio, HistorialAdmin)