from django.shortcuts import render
from django.shortcuts import redirect
from shared.models import *
from model.models import Application


def index(request):
    properties = []
    objects = RestrictedProduct.objects.all()
    for object in objects:
        object.properties = []
        object.properties.append({'name': 'product_number', 'type': 'string', 'value': object.product_number})
        object.properties.append({'name': 'price', 'type': 'string', 'value': object.price})
        object.properties.append({'name': 'name', 'type': 'string', 'value': object.name})
        object.properties.append({'name': 'location', 'type': 'string', 'value': object.location})
        object.properties.append({'name': 'description', 'type': 'string', 'value': object.description})
        object.properties.reverse()
    properties.append({'name': 'description'})
    properties.append({'name': 'location'})
    properties.append({'name': 'name'})
    properties.append({'name': 'price'})
    properties.append({'name': 'product_number'})
    context = {'application': __get_application(request), 'properties': properties, 'objects': objects, 'object_name': 'RestrictedProduct', 'object_name_lower': 'restrictedproduct'}
    return render(request, 'view_list.html', context)


def add(request):
    properties = []
    properties.append({'type': 'string', 'name': 'product_number'})
    properties.append({'type': 'string', 'name': 'price'})
    properties.append({'type': 'string', 'name': 'name'})
    properties.append({'type': 'string', 'name': 'location'})
    properties.append({'type': 'string', 'name': 'description'})
    if request.method == 'GET':
        properties.reverse()
        add_objects = []
        add_context = {
             'application': __get_application(request),
             'properties': properties,
             'object_name': 'RestrictedProduct',
             'object_name_lower': 'restrictedproduct'
        }
        return render(request, 'add_object.html', add_context)

    description = request.POST['description']
    location = request.POST['location']
    name = request.POST['name']
    price = request.POST['price']
    product_number = request.POST['product_number']
    restrictedproduct = RestrictedProduct(description=description, location=location, name=name, price=price, product_number=product_number)
    restrictedproduct.save()

    return redirect('/' + __get_application(request).name + '/restrictedproduct')


def edit(request, id):
    properties = []
    restrictedproduct = RestrictedProduct.objects.get(id=id)
    properties.append({'type': 'string', 'name': 'product_number', 'value': restrictedproduct.product_number})
    properties.append({'type': 'string', 'name': 'price', 'value': restrictedproduct.price})
    properties.append({'type': 'string', 'name': 'name', 'value': restrictedproduct.name})
    properties.append({'type': 'string', 'name': 'location', 'value': restrictedproduct.location})
    properties.append({'type': 'string', 'name': 'description', 'value': restrictedproduct.description})
    if request.method == 'GET':
        properties.reverse()
        edit_objects = []
        edit_context = {
             'application': __get_application(request),
             'object_id': id,
             'properties': properties,
             'object_name': 'RestrictedProduct',
             'object_name_lower': 'restrictedproduct'
        }
        return render(request, 'edit_object.html', edit_context)

    restrictedproduct.description = request.POST['description']
    restrictedproduct.location = request.POST['location']
    restrictedproduct.name = request.POST['name']
    restrictedproduct.price = request.POST['price']
    restrictedproduct.product_number = request.POST['product_number']
    restrictedproduct.save()

    return redirect('/' + __get_application(request).name + '/restrictedproduct')


def delete(request, id):
    restrictedproduct = RestrictedProduct.objects.get(id=id)
    restrictedproduct.delete()
    return redirect('/' + __get_application(request).name + '/restrictedproduct')


def __get_application(request):
    application_name_lower = request.build_absolute_uri().split('/')[3]
    application = Application.objects.get(name=application_name_lower)
    return application
