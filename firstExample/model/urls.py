from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('applications/', views.applications.index),
    path('applications/add', views.applications.add),
    path('applications/<application_id>', views.applications.view),
    path('applications/<application_id>/addclassifier', views.applications.add_classifier),
    path('applications/<application_id>/delete', views.applications.delete),
    path('applications/<application_id>/<classifier_id>/unlink', views.applications.unlink),
    path('applications/<application_id>/<classifier_id>/properties', views.applications.properties),
    path('classifiers/', views.classifiers.index),
    path('classifiers/add', views.classifiers.add),
    path('classifiers/<classifier_id>', views.classifiers.edit),
    path('classifiers/<classifier_id>/delete', views.classifiers.delete),
    path('properties/add', views.properties.add),
    path('properties/<property_id>/edit', views.properties.edit),
    path('properties/<property_id>/delete', views.properties.delete),
    path('operations/add', views.operations.add),
    path('operations/<operation_id>', views.operations.edit),
    path('operations/<operation_id>/delete', views.operations.delete),
    path('operations/parameters/add', views.operation_parameters.add),
    path('operations/parameters/<operation_parameter_id>/delete', views.operation_parameters.delete),
    path('relationships/', views.relationships.index),
    path('relationships/add', views.relationships.add),
    path('relationships/add/generalization', views.relationships.add_generalization),
    path('relationships/add/association', views.relationships.add_association),
    path('relationships/<relationship_id>/delete', views.relationships.delete),
    path('generate', views.generate),
    path('diagram', views.diagram)
]
