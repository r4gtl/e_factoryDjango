from django.urls import path
from . import views


urlpatterns = [
    path('new-supplier/', views.CreateSupplier.as_view(), name="create-supplier"),
    path('update-supplier/<int:pk>/', views.UpdateSupplier.as_view(), name="update-supplier"),
    path('search/', views.searchSupplier, name='search-supplier'),
]