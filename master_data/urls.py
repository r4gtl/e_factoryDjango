from django.urls import path
from . import views


urlpatterns = [
    path('new-supplier/', views.CreateSupplier.as_view(), name="create-supplier"),
    # path('update-supplier/<int:pk>/', views.UpdateSupplier.as_view(), name="update-supplier"),
    path('update-supplier/<int:pk>/', views.update_supplier, name="update-supplier"),
    path('update-supplier/<int:pk>/new-contact', views.new_contact, name="new-contact"),
    path('search/', views.searchSupplier, name='search-supplier'),
]



 #path(
  #      "operatore/<int:pk>/aggiungi-incarico/",
   #     views.aggiungi_nomeincarico,
    #    name="aggiungi_incarico"
    #)#,
