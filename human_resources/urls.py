from django.urls import path

from . import views

app_name = 'human_resources'

urlpatterns = [
    path('human_resources/', views.human_resources_home, name="human_resources"),
    
]