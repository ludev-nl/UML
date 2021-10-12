from django.shortcuts import render
from django.shortcuts import redirect
from ..models import *
from ..generators import *
import pprint


def index(request):
    application_list = Application.objects.all()
    context = {
        'applications': application_list
    }
    return render(request, 'applications.html', context)


def add(request):
    if request.method == 'GET':
        return render(request, 'add_application.html')

    name = request.POST['name']

    application = Application(name=name.lower())
    application.save()

    ApplicationGenerator(application).generate()

    return redirect('/model/applications')


def view(request, application_id):
    classifiers_to_add = Classifier.objects.all()
    application = Application.objects.get(id=application_id)
    categories = application.categories.all()
    classifiers = application.classifiers.all()
    for classifier in [x for x in classifiers]:
        classifier.properties = Property.objects.filter(classifier=classifier, applications=application).all()
        # classifier.operations = Operation.objects.filter(classifier_id=classifier.id)
    classifiers_to_add = [x for x in classifiers_to_add if x not in classifiers]
    for classifier in classifiers:
        classifier.name_lower = classifier.name.lower()
    context = {
        'application': application,
        'classifiers': classifiers,
        'categories': categories,
        'classifiers_to_add': classifiers_to_add
    }

    return render(request, 'application_view.html', context)


def add_classifier(request, application_id):
    application = Application.objects.get(id=application_id)
    classifier = Classifier.objects.get(id=request.POST['classifier_id'])
    application.classifiers.add(classifier)
    application.save()

    ClassifierGenerator(classifier).link_application(application_id)

    return redirect('/model/applications/' + application_id)


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


def delete_page(request, application_id, page_id):
    page = Page.objects.get(id=page_id)
    category = page.category.get()
    page.delete()
    category.page_set.remove(page)
    return redirect('/model/applications/' + application_id)


def unlink(request, application_id, classifier_id):
    classifier = Classifier.objects.get(id=classifier_id)
    application = Application.objects.get(id=application_id)
    application.classifiers.remove(classifier)
    application.save()
    ClassifierGenerator(classifier).unlink_application(application)

    return redirect('/model/applications/' + application_id)


def delete(request, application_id):
    application = Application.objects.get(id=application_id)
    application.delete()

    ApplicationGenerator(application).delete()

    return redirect('/model/applications')


def properties(request, application_id, classifier_id):
    application = Application.objects.get(id=application_id)
    classifier = Classifier.objects.get(id=classifier_id)
    properties = Property.objects.filter(classifier=classifier).all()
    if request.method == 'GET':
        for property in properties:
            property.linked = False
            if application in property.applications.all():
                property.linked = True

        context = {
            'properties': properties,
            'application': application,
            'classifier': classifier
        }
        return render(request, 'application_link_properties.html', context)

    for property in properties:
        if property.name in request.POST:
            if application not in property.applications.all():
                property.applications.add(application)
                PropertyGenerator(property).link_to_application(application)
        else:
            if application in property.applications.all():
                property.applications.remove(application)
                PropertyGenerator(property).unlink_from_application(application)

    return redirect('/model/applications/' + application_id)

