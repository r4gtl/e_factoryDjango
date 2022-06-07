from django.urls import path
from . import views

app_name = 'chemicals'

urlpatterns = [
    path('supplier-list/', views.home, name="search-supplier"),
    path('price-list/<int:pk>/', views.price_list, name="price-list"),
    path('single-product/<int:pk>/', views.update_product, name="single-product"),    
    path('single-product/<int:pk>/create-product/', views.new_product, name="create-product"),
    path('elimina-prodotto/<int:pk>/', views.delete_product, name="cancella_prodotto"),
    path('single-product/<int:pk>/new-sds/', views.new_sds, name="new-sds"),     
]