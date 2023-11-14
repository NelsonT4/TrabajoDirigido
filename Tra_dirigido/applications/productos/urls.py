from django.urls import path
from . import views


app_name = "productos_app"
urlpatterns = [
    path('ProductsPrice/',
         views.getProductoByPrice.as_view(),
         name="producto"
         ),
]