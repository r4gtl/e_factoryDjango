from django.urls import path
from . import views


urlpatterns = [
    path('new-supplier/', views.CreateSupplier.as_view(), name="create-supplier"),
    # path('update-supplier/<int:pk>/', views.UpdateSupplier.as_view(), name="update-supplier"),
    path('update-supplier/<int:pk>/', views.update_supplier, name="update-supplier"),
    path('update-supplier/<int:pk>/new-contact/', views.new_contact, name="new-contact"),
    #path('update-supplier/<int:id>/update-contact/<int:pk>/', views.update_contact, name="update-contact"),
    path('update-supplier/<int:id>/update-contact/<int:pk>/', views.UpdateContact.as_view(), name="update-contact"),
    path('search/', views.searchSupplier, name='search-supplier'),
]