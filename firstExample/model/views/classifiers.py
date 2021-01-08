from django.shortcuts import render
from django.shortcuts import redirect
from ..models import Classifier, Property, Operation, Class, Enumerator, OperationParameter
from ..enums import Type
from ..generators import *


def index(request):
    classifier_list = Classifier.objects.all()
    for classifier in classifier_list:
        classifier.properties = Property.objects.filter(classifier_id=classifier.id)
        classifier.operations = Operation.objects.filter(classifier_id=classifier.id)
    context = {
        'classifiers': classifier_list
    }
    return render(request, 'classifiers.html', context)


def add(request):
    if request.method == 'GET':
        context = {
            'types': [cls.__name__ for cls in Classifier.__subclasses__()]
        }

        return render(request, 'add_classifier.html', context)

    name = request.POST['name']
    classifier_type = request.POST['type']

    if classifier_type == 'Class':
        classifier = Class(name=name)
        classifier.save()
    elif classifier_type == 'Enumerator':
        classifier = Enumerator(name=name)
        classifier.save()
    else:
        raise NotImplementedError

    ClassifierGenerator(classifier).generate()

    return redirect('/model/classifiers')


def edit(request, classifier_id):
    classifier = Classifier.objects.get(id=classifier_id)
    classifier.properties = Property.objects.filter(classifier_id=classifier_id)
    classifier.operations = Operation.objects.filter(classifier_id=classifier_id)
    for operation in classifier.operations:
        operation.parameters = OperationParameter.objects.filter(operation_id=operation.id)
        parameter_string = ''
        for parameter in operation.parameters:
            if parameter_string.__len__() > 0:
                parameter_string += ', '

            parameter_string += parameter.type + ' ' + parameter.name
        operation.name = operation.name + '(' + parameter_string + ')'
    types = [type.value for type in Type]
    context = {
        'classifier': classifier,
        'types': types
    }
    return render(request, 'edit_classifier.html', context)


def delete(request, classifier_id):
    classifier = Classifier.objects.get(id=classifier_id)

    ClassifierGenerator(classifier).delete()
    classifier.delete()

    return redirect('/model/classifiers')


def add_operation(request, classifier_id):
    classifier = Classifier.objects.get(id=classifier_id)
    return_type = request.POST['type']
    implementation = request.POST['implementation']
    name = request.POST['name']

    if return_type is 'string':
        return_type = Type.String
    elif return_type is 'int':
        return_type = Type.Int
    elif return_type is 'bool':
        return_type = Type.Bool

    operation = Operation(name=name, type=return_type, implementation=implementation, classifier=classifier)
    operation.save()
    return redirect('/model/classifiers/' + classifier_id)
