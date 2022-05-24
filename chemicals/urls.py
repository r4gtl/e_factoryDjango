from django.urls import path
from . import views

app_name = 'chemicals'

urlpatterns = [
    path('supplier-list/', views.home, name="search-supplier"),
    path('price-list/<int:pk>/', views.price_list, name="price-list"),
    path('single-product/<int:pk>/', views.update_product, name="single-product"),
]