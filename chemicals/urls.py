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
    path('single-product/<int:id>/update-sds/<int:pk>/', views.UpdateSds.as_view(), name="update-sds"),
    path('update-sds/<int:pk>/new-substance/', views.new_substance_sds, name="new-substance-sds"),
    path('update-sds/<int:pk>/new-ps-sds/', views.new_ps_sds, name="new-ps-sds"),
    path('update-sds/<int:pk>/new-hs-sds/', views.new_hs_sds, name="new-hs-sds"),
    
]