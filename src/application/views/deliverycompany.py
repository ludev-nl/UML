from django.shortcuts import render
from django.shortcuts import redirect
from shared.models import *
from model.models import Application


def index(request):
    properties = []
    objects = DeliveryCompany.objects.all()
    for object in objects:
        object.properties = []
        object.properties.append({'name': 'name', 'type': 'string', 'value': object.name})
        object.properties.append({'name': 'address', 'type': 'string', 'value': object.address})
        object.properties.reverse()
    properties.append({'name': 'address'})
    properties.append({'name': 'name'})
    context = {'application': __get_application(request), 'properties': properties, 'objects': objects, 'object_name': 'DeliveryCompany', 'object_name_lower': 'deliverycompany'}
    return render(request, 'view_list.html', context)


def add(request):
    properties = []
    properties.append({'type': 'string', 'name': 'name'})
    properties.append({'type': 'string', 'name': 'address'})
    if request.method == 'GET':
        properties.reverse()
        add_objects = []
        add_context = {
             'application': __get_application(request),
             'properties': properties,
             'object_name': 'DeliveryCompany',
             'object_name_lower': 'deliverycompany'
        }
        return render(request, 'add_object.html', add_context)

    address = request.POST['address']
    name = request.POST['name']
    deliverycompany = DeliveryCompany(address=address, name=name)
    deliverycompany.save()

    return redirect('/' + __get_application(request).name + '/deliverycompany')


def edit(request, id):
    properties = []
    deliverycompany = DeliveryCompany.objects.get(id=id)
    properties.append({'type': 'string', 'name': 'name', 'value': deliverycompany.name})
    properties.append({'type': 'string', 'name': 'address', 'value': deliverycompany.address})
    if request.method == 'GET':
        properties.reverse()
        edit_objects = []
        edit_context = {
             'application': __get_application(request),
             'object_id': id,
             'properties': properties,
             'object_name': 'DeliveryCompany',
             'object_name_lower': 'deliverycompany'
        }
        return render(request, 'edit_object.html', edit_context)

    deliverycompany.address = request.POST['address']
    deliverycompany.name = request.POST['name']
    deliverycompany.save()

    return redirect('/' + __get_application(request).name + '/deliverycompany')


def delete(request, id):
    deliverycompany = DeliveryCompany.objects.get(id=id)
    deliverycompany.delete()
    return redirect('/' + __get_application(request).name + '/deliverycompany')


def __get_application(request):
    application_name_lower = request.build_absolute_uri().split('/')[3]
    application = Application.objects.get(name=application_name_lower)
    return application
