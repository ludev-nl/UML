from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add/', views.add),
    path('remove', views.remove),
    path('modified/', views.get_modified_rules)
]
