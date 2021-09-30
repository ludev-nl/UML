from django.shortcuts import render
from django.shortcuts import redirect
from shared.models import *
from model.models import Application


def index(request):
    properties = []
    objects = Order.objects.all()
    for object in objects:
        object.properties = []
        object.properties.append({'name': 'entry_date', 'type': 'string', 'value': object.entry_date})
        object.properties.append({'name': 'description', 'type': 'string', 'value': object.description})
        object.properties.append({'name': 'order_number', 'type': 'int', 'value': object.order_number})
        object.properties.append({'name': 'delivery_status', 'type': 'string', 'value': object.delivery_status})
        object.properties.append({'name': 'DeliveryCompany', 'type': 'association', 'value': object.deliverycompany.__str__})
        object.properties.append({'name': 'Customer', 'type': 'association', 'value': object.customer.__str__})
        object.properties.reverse()
    properties.append({'name': 'Customer'})
    properties.append({'name': 'DeliveryCompany'})
    properties.append({'name': 'delivery_status'})
    properties.append({'name': 'order_number'})
    properties.append({'name': 'description'})
    properties.append({'name': 'entry_date'})
    context = {'application': __get_application(request), 'properties': properties, 'objects': objects, 'object_name': 'Order', 'object_name_lower': 'order'}
    return render(request, 'view_list.html', context)


def add(request):
    properties = []
    properties.append({'type': 'string', 'name': 'entry_date'})
    properties.append({'type': 'string', 'name': 'description'})
    properties.append({'type': 'int', 'name': 'order_number'})
    properties.append({'type': 'string', 'name': 'delivery_status'})
    properties.append({'type': 'association', 'name': 'deliverycompany'})
    properties.append({'type': 'association', 'name': 'customer'})
    if request.method == 'GET':
        properties.reverse()
        add_objects = []
        add_objects.append({'name': 'deliverycompany', 'values': DeliveryCompany.objects.all()})
        add_objects.append({'name': 'customer', 'values': Customer.objects.all()})
        add_context = {
             'objects': add_objects,
             'objects': add_objects,
             'application': __get_application(request),
             'properties': properties,
             'object_name': 'Order',
             'object_name_lower': 'order'
        }
        return render(request, 'add_object.html', add_context)

    customer_id = request.POST['customer']
    customer = Customer.objects.get(id=customer_id)
    deliverycompany_id = request.POST['deliverycompany']
    deliverycompany = DeliveryCompany.objects.get(id=deliverycompany_id)
    delivery_status = request.POST['delivery_status']
    order_number = request.POST['order_number']
    description = request.POST['description']
    entry_date = request.POST['entry_date']
    order = Order(customer=customer, deliverycompany=deliverycompany, delivery_status=delivery_status, order_number=order_number, description=description, entry_date=entry_date)
    order.save()

    return redirect('/' + __get_application(request).name + '/order')


def edit(request, id):
    properties = []
    order = Order.objects.get(id=id)
    properties.append({'type': 'string', 'name': 'entry_date', 'value': order.entry_date})
    properties.append({'type': 'string', 'name': 'description', 'value': order.description})
    properties.append({'type': 'int', 'name': 'order_number', 'value': order.order_number})
    properties.append({'type': 'string', 'name': 'delivery_status', 'value': order.delivery_status})
    properties.append({'type': 'association', 'name': 'deliverycompany', 'value': order.deliverycompany.__str__})
    properties.append({'type': 'association', 'name': 'customer', 'value': order.customer.__str__})
    if request.method == 'GET':
        properties.reverse()
        edit_objects = []
        edit_objects.append({'name': 'deliverycompany', 'values': DeliveryCompany.objects.all()})
        edit_objects.append({'name': 'customer', 'values': Customer.objects.all()})
        edit_context = {
             'objects': edit_objects,
             'objects': edit_objects,
             'application': __get_application(request),
             'object_id': id,
             'properties': properties,
             'object_name': 'Order',
             'object_name_lower': 'order'
        }
        return render(request, 'edit_object.html', edit_context)

    order.customer = Customer.objects.get(id=request.POST['customer'])
    order.deliverycompany = DeliveryCompany.objects.get(id=request.POST['deliverycompany'])
    order.delivery_status = request.POST['delivery_status']
    order.order_number = request.POST['order_number']
    order.description = request.POST['description']
    order.entry_date = request.POST['entry_date']
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
