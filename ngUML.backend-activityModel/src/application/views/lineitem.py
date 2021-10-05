from django.shortcuts import render
from django.shortcuts import redirect
from shared.models import *
from model.models import Application


def index(request):
    properties = []
    objects = LineItem.objects.all()
    for object in objects:
        object.properties = []
        object.properties.append({'name': 'quantity', 'type': 'int', 'value': object.quantity})
        object.properties.append({'name': 'Product', 'type': 'association', 'value': object.product.__str__})
        object.properties.append({'name': 'Order', 'type': 'association', 'value': object.order.__str__})
        object.properties.reverse()
    properties.append({'name': 'Order'})
    properties.append({'name': 'Product'})
    properties.append({'name': 'quantity'})
    context = {'application': __get_application(request), 'properties': properties, 'objects': objects, 'object_name': 'LineItem', 'object_name_lower': 'lineitem'}
    return render(request, 'view_list.html', context)


def add(request):
    properties = []
    properties.append({'type': 'int', 'name': 'quantity'})
    properties.append({'type': 'association', 'name': 'product'})
    properties.append({'type': 'association', 'name': 'order'})
    if request.method == 'GET':
        properties.reverse()
        add_objects = []
        add_objects.append({'name': 'product', 'values': Product.objects.all()})
        add_objects.append({'name': 'order', 'values': Order.objects.all()})
        add_context = {
             'objects': add_objects,
             'objects': add_objects,
             'application': __get_application(request),
             'properties': properties,
             'object_name': 'LineItem',
             'object_name_lower': 'lineitem'
        }
        return render(request, 'add_object.html', add_context)

    order_id = request.POST['order']
    order = Order.objects.get(id=order_id)
    product_id = request.POST['product']
    product = Product.objects.get(id=product_id)
    quantity = request.POST['quantity']
    lineitem = LineItem(order=order, product=product, quantity=quantity)
    lineitem.save()

    return redirect('/' + __get_application(request).name + '/lineitem')


def edit(request, id):
    properties = []
    lineitem = LineItem.objects.get(id=id)
    properties.append({'type': 'int', 'name': 'quantity', 'value': lineitem.quantity})
    properties.append({'type': 'association', 'name': 'product', 'value': lineitem.product.__str__})
    properties.append({'type': 'association', 'name': 'order', 'value': lineitem.order.__str__})
    if request.method == 'GET':
        properties.reverse()
        edit_objects = []
        edit_objects.append({'name': 'product', 'values': Product.objects.all()})
        edit_objects.append({'name': 'order', 'values': Order.objects.all()})
        edit_context = {
             'objects': edit_objects,
             'objects': edit_objects,
             'application': __get_application(request),
             'object_id': id,
             'properties': properties,
             'object_name': 'LineItem',
             'object_name_lower': 'lineitem'
        }
        return render(request, 'edit_object.html', edit_context)

    lineitem.order = Order.objects.get(id=request.POST['order'])
    lineitem.product = Product.objects.get(id=request.POST['product'])
    lineitem.quantity = request.POST['quantity']
    lineitem.save()

    return redirect('/' + __get_application(request).name + '/lineitem')


def delete(request, id):
    lineitem = LineItem.objects.get(id=id)
    lineitem.delete()
    return redirect('/' + __get_application(request).name + '/lineitem')


def __get_application(request):
    application_name_lower = request.build_absolute_uri().split('/')[3]
    application = Application.objects.get(name=application_name_lower)
    return application
