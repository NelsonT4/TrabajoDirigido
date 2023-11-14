from django.contrib import admin
from .models import Productos
# Register your models here.



class  ProductosAdmin(admin.ModelAdmin):
    list_display = (
        'productId',
        'store',
        'name',
        'category',
        'make',
        'describe',
        'basicNeed',
    )


admin.site.register(Productos, ProductosAdmin)