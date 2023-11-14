from django.contrib import admin
from .models import Usuarios

# Register your models here.
class UsuariosAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'key',
        'intervalHistory'
    )

admin.site.register(Usuarios)