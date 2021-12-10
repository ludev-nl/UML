from django.shortcuts import render
from django.shortcuts import redirect
from shared.models import *
from model.models import Application


def index(request):
    properties = []
    objects = Order.objects.all()
    for object in objects:
        object.properties = []
        object.properties.append({'name': 'DeliveryCompany', 'type': 'association', 'value': object.deliverycompany.__str__})
        object.properties.reverse()
    properties.append({'name': 'DeliveryCompany'})
    context = {'application': __get_application(request), 'properties': properties, 'objects': objects, 'object_name': 'Order', 'object_name_lower': 'order'}
    return render(request, 'view_list.html', context)


def add(request):
    properties = []
    properties.append({'type': 'association', 'name': 'deliverycompany'})
    if request.method == 'GET':
        properties.reverse()
        add_objects = []
        add_objects.append({'name': 'deliverycompany', 'values': DeliveryCompany.objects.all()})
        add_context = {
             'objects': add_objects,
             'application': __get_application(request),
             'properties': properties,
             'object_name': 'Order',
             'object_name_lower': 'order'
        }
        return render(request, 'add_object.html', add_context)

    deliverycompany_id = request.POST['deliverycompany']
    deliverycompany = DeliveryCompany.objects.get(id=deliverycompany_id)
    order = Order(deliverycompany=deliverycompany)
    order.save()

    return redirect('/' + __get_application(request).name + '/order')


def edit(request, id):
    properties = []
    order = Order.objects.get(id=id)
    properties.append({'type': 'association', 'name': 'deliverycompany', 'value': order.deliverycompany.__str__})
    if request.method == 'GET':
        properties.reverse()
        edit_objects = []
        edit_objects.append({'name': 'deliverycompany', 'values': DeliveryCompany.objects.all()})
        edit_context = {
             'objects': edit_objects,
             'application': __get_application(request),
             'object_id': id,
             'properties': properties,
             'object_name': 'Order',
             'object_name_lower': 'order'
        }
        return render(request, 'edit_object.html', edit_context)

    order.deliverycompany = DeliveryCompany.objects.get(id=request.POST['deliverycompany'])
    order.save()

    return redirect('/' + __get_application(request).name + '/order')


def delete(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect('/' + __get_application(request).name + '/order')


def __get_application(request):
    application_name_lower = request.build_absolute_uri().split('/')[3]
    application = Application.objects.get(name=application_name_lower)
    return application
