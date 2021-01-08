# from django.shortcuts import render
from django.shortcuts import redirect
from ..models import Classifier, Operation, Property
from ..enums import Type
from ..generators import *


def delete(request, property_id):
    property = Property.objects.get(id=property_id)
    classifier_id = str(property.classifier.id)

    PropertyGenerator(property).delete()
    property.delete()

    return redirect('/model/classifiers/' + classifier_id)


def add(request):
    classifier_id = request.POST['classifier_id']
    classifier = Classifier.objects.get(id=classifier_id)
    prop_type = request.POST['type']

    if prop_type is 'string':
        prop_type = Type.String
    elif prop_type is 'int':
        prop_type = Type.Int
    elif prop_type is 'bool':
        prop_type = Type.Bool

    property = Property(name=request.POST['name'], type=prop_type, classifier=classifier)
    property.save()

    PropertyGenerator(property).generate()

    return redirect('/model/classifiers/' + classifier_id)