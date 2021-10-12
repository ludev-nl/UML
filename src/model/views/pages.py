from django.shortcuts import render
from django.shortcuts import redirect
from ..models import *
import os
from ..generators import *
import pprint

def add_category(request, application_id):
    application = Application.objects.get(id=application_id)
    if request.method == 'GET':
        context = {
            'application': application,
        }
        return render(request, 'add_category.html', context)
    else:
        name = request.POST['name']
        category = Category(name=name.lower())
        category.save()
        application.categories.add(category)
        return redirect('/model/applications/' + application_id)


def add_page(request, application_id, category_id):
    application = Application.objects.get(id=application_id)
    category = application.categories.filter(id=category_id).get()
    if request.method == 'GET':
        context = {
            'application': application,
            'category': category
        }
        return render(request, 'add_page.html', context)
    else:
        name = request.POST['name']
        page = Page(name=name.lower())
        page.save()
        page.category.add(category)
        return redirect('/model/applications/' + application_id + '/category/' + category_id)


def show_category(request, application_id, category_id):
    application = Application.objects.get(id=application_id)
    category = application.categories.filter(id=category_id).get()
    pages = category.page_set.all()
    context = {
        'application': application,
        'category': category,
        'pages': pages,
    }
    return render(request, 'show_category.html', context)


def edit_category(request, application_id, category_id):
    return redirect('/model/applications/' + application_id)


def delete_category(request, application_id, category_id):
    application = Application.objects.get(id=application_id)
    category = application.categories.filter(id=category_id).get()
    category.delete()
    application.categories.remove(category)
    return redirect('/model/applications/' + application_id)


def page_link_properties(request, application_id, page_id):
    application = Application.objects.get(id=application_id)
    classifiers = application.classifiers.all()
    page = Page.objects.get(id=page_id)
    allProperties = application.property_set
    if request.method == "GET":
        for classifier in [x for x in classifiers]:
            classifier.properties = []
            thisProperties = allProperties.filter(classifier=classifier.id).all()
            selectedProperties = page.property_set.all()
            for property in [x for x in thisProperties]:
                if property in selectedProperties:
                    property.linked = True
                classifier.properties.append(property)

            print(classifier.properties)
        context = {
            'application': application,
            'page': page,
            'classifiers': classifiers,
        }
        return render(request, 'page_link_properties.html', context)
    else:

        for property in allProperties.all():
            if property.name in request.POST:
                if page not in property.applications.all():
                    property.applications.add(page)
            else:
                if page in property.applications.all():
                    property.applications.remove(page)

        return redirect('/model/applications/' + application_id + '/page/' + page_id + '/properties')


def show_page(request, application_id, page_id):
    return redirect('/model/applications/' + application_id)


def edit_page(request, application_id, page_id):
    application = Application.objects.get(id=application_id)
    page = Page.objects.get(id=page_id)
    context = {
        'application': application,
        'page': page,
    }
    return render(request, 'page_edit.html',context)


def delete_page(request, application_id, page_id):
    page = Page.objects.get(id=page_id)
    category = page.category.get()
    page.delete()
    category.page_set.remove(page)
    return redirect('/model/applications/' + application_id)

