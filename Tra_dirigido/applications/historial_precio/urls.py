from django.contrib import admin
from django.urls import path
from . import views

app_name = "historial_app"

urlpatterns = [
    path('history/',
         views.ListaHistorialPrecio.as_view(),
        name="historial"),
    path('historial/<id>',
         views.ListaHistorial.as_view(),
        name="historia"),
]
