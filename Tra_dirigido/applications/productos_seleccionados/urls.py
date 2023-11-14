from django.urls import path
from . import views



urlpatterns = [
    path('productsSelect/', views.IndexView.as_view()),
]