from django.urls import path
from . import views


urlpatterns = [
    path('new-supplier/', views.CreateSupplier.as_view(), name="create-supplier"),
    path('search/', views.searchSupplier, name='search-supplier'),
]