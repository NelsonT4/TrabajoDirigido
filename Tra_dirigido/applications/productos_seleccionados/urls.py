from django.urls import path
from . import views

app_name = "productosSeleccionado_app"

urlpatterns = [
    path('productsSelect/<pk>',
         views.IndexView.as_view(),
         name='producto-seleccionados'),
]
