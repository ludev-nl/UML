from django.shortcuts import render
from django.shortcuts import redirect
from ..models import Classifier, Operation, OperationParameter
from ..enums import Type


def edit(request, operation_id):
    operation = Operation.objects.get(id=operation_id)
    types = [type.value for type in Type]
    context = {
        'operation': operation,
        'parameters': OperationParameter.objects.all(),
        'types': types
    }

    return render(request, 'edit_operation.html', context)


def add(request):
    classifier_id = request.POST['classifier_id']
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


def delete(request, operation_id):
    operation = Operation.objects.get(id=operation_id)
    classifier = operation.classifier
    operation.delete()
    return redirect('/model/classifiers/' + str(classifier.id))