from django.urls import path
from . import views

app_name = 'chemicals'

urlpatterns = [
    path('supplier-list/', views.home, name="search-supplier"),
    path('new-order/', views.CreateOrder.as_view(), name="new-order"),
    path('update-order/<int:pk>/', views.UpdateOrder.as_view(), name="update-order"),
    path('update-order/<int:pk>/add-detail/', views.create_detail, name="add-detail"),
    path('orders-list/', views.OrderList.as_view(), name="orders-list"),
    path('price-list/<int:pk>/', views.price_list, name="price-list"),
    path('single-product/<int:pk>/', views.update_product, name="single-product"),    
    path('single-product/<int:pk>/create-product/', views.new_product, name="create-product"),
    path('elimina-prodotto/<int:pk>/', views.delete_product, name="cancella_prodotto"),
    path('single-product/<int:pk>/new-sds/', views.new_sds, name="new-sds"),
    path('single-product/<int:id>/update-sds/<int:pk>/', views.UpdateSds.as_view(), name="update-sds"),    
    path('update-sds/<int:pk>/new-substance/', views.new_substance_sds, name="new-substance-sds"),
    path('update-sds/<int:pk>/new-ps-sds/', views.new_ps_sds, name="new-ps-sds"),
    path('update-sds/<int:pk>/new-hs-sds/', views.new_hs_sds, name="new-hs-sds"),
    path('single-product/<int:id>/update-sds/<int:pk>/new-ds-sds/', views.new_ds_sds, name="new-ds-sds"),

    path('data/<int:id_chemical>/', views.load_last_orders_view, name='last-orders' ),
    path('chemlist/<int:id_supplier>/<int:num_chems>/', views.load_chemicals_to_search, name='load-chemicals' ),
    path('chemlist/<int:id_supplier>/<str:search_text>/<int:num_chems>/', views.load_chemicals_to_search_filtered, name='load-chemicals-filtered' ),
    path('supplier_list/', views.load_suppliers_to_search, name='load-suppliers-search' ),
    path('supplier_list/<str:search_text>/', views.load_suppliers_to_search_filtered, name='load-suppliers-search-filtered'),
    path('<int:pk>/update_conformity/', views.update_conf_order, name='update-conformity'),
    path('substances-list/', views.load_substances_to_search, name='load-substances-search'),
    #path('data/<str:search_description>/<str:search_cas>/<str:search_ec>/', views.load_substances_to_search_filtered, name='load-substances-search-filtered'),
    path('substance/<str:search_cas>/', views.load_substances_to_search_filtered, name='load-substances-search-filtered'),
]