from django.shortcuts import render
from django.shortcuts import redirect
from shared.models import *
from model.models import Application


def index(request):
    properties = []
    objects = Customer.objects.all()
    for object in objects:
        object.properties = []
        object.properties.append({'name': 'address', 'type': 'string', 'value': object.address})
        object.properties.append({'name': 'last_name', 'type': 'string', 'value': object.last_name})
        object.properties.append({'name': 'birth_date', 'type': 'string', 'value': object.birth_date})
        object.properties.append({'name': 'first_name', 'type': 'string', 'value': object.first_name})
        object.properties.append({'name': 'name', 'type': 'string', 'value': object.name})
        object.properties.reverse()
    properties.append({'name': 'name'})
    properties.append({'name': 'first_name'})
    properties.append({'name': 'birth_date'})
    properties.append({'name': 'last_name'})
    properties.append({'name': 'address'})
    context = {'application': __get_application(request), 'properties': properties, 'objects': objects, 'object_name': 'Customer', 'object_name_lower': 'customer'}
    return render(request, 'view_list.html', context)


def add(request):
    properties = []
    properties.append({'type': 'string', 'name': 'address'})
    properties.append({'type': 'string', 'name': 'last_name'})
    properties.append({'type': 'string', 'name': 'birth_date'})
    properties.append({'type': 'string', 'name': 'first_name'})
    properties.append({'type': 'string', 'name': 'name'})
    if request.method == 'GET':
        properties.reverse()
        add_objects = []
        add_context = {
             'application': __get_application(request),
             'properties': properties,
             'object_name': 'Customer',
             'object_name_lower': 'customer'
        }
        return render(request, 'add_object.html', add_context)

    name = request.POST['name']
    first_name = request.POST['first_name']
    birth_date = request.POST['birth_date']
    last_name = request.POST['last_name']
    address = request.POST['address']
    customer = Customer(name=name, first_name=first_name, birth_date=birth_date, last_name=last_name, address=address)
    customer.save()

    return redirect('/' + __get_application(request).name + '/customer')


def edit(request, id):
    properties = []
    customer = Customer.objects.get(id=id)
    properties.append({'type': 'string', 'name': 'address', 'value': customer.address})
    properties.append({'type': 'string', 'name': 'last_name', 'value': customer.last_name})
    properties.append({'type': 'string', 'name': 'birth_date', 'value': customer.birth_date})
    properties.append({'type': 'string', 'name': 'first_name', 'value': customer.first_name})
    properties.append({'type': 'string', 'name': 'name', 'value': customer.name})
    if request.method == 'GET':
        properties.reverse()
        edit_objects = []
        edit_context = {
             'application': __get_application(request),
             'object_id': id,
             'properties': properties,
             'object_name': 'Customer',
             'object_name_lower': 'customer'
        }
        return render(request, 'edit_object.html', edit_context)

    customer.name = request.POST['name']
    customer.first_name = request.POST['first_name']
    customer.birth_date = request.POST['birth_date']
    customer.last_name = request.POST['last_name']
    customer.address = request.POST['address']
    customer.save()

    return redirect('/' + __get_application(request).name + '/customer')


def delete(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('/' + __get_application(request).name + '/customer')


def __get_application(request):
    application_name_lower = request.build_absolute_uri().split('/')[3]
    application = Application.objects.get(name=application_name_lower)
    return application
