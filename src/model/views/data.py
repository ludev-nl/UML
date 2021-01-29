from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Class, Classifier, Property, Operation, Generalization, OperationParameter, Association, Composition, Relationship
from ..generators import *
import os
import json
import uuid

def classifierToOperations(classifier):
    operations = Operation.objects.filter(
        classifier=classifier
    )

    return [
        {
            'name': operation.name,
            'type': operation.type,
            'code': operation.implementation,
            'id': operation.id
        } for operation in operations
    ]

def classifierToProperties(classifier):
    properties = Property.objects.filter(
        classifier=classifier
    )

    return [
        {
            'name': prop.name,
            'type': prop.type,
            'id': prop.id
        } for prop in properties
    ]

def classifierToNode(classifier):
    return {
        'type': 'Class',
        'name': str(classifier),
        'data': {
            'properties': classifierToProperties(classifier),
            'methods': classifierToOperations(classifier)
        },
        'instances': {},
        'id': classifier.id
    }

def getUUIDfromClassifier(classifier, nodes):
    for key, value in nodes.items():
        if value.get('name') == classifier:
            return key
    return ''

def processToBackend(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    for item in body_data:
        if item.get('type') == 'delete-property':
            Property.objects.filter(id=item.get('id')).delete()
        if item.get('type') == 'add-property':
            classifier = Classifier.objects.filter(name=item.get('key').get('name'))
            Property.objects.create(
                name=item.get('to').get('name'),
                type=item.get('to').get('type'),
                classifier=classifier
            )
        if item.get('type') == 'delete-method':
            Operation.objects.filter(id=item.get('id')).delete()
        if item.get('type') == 'add-method':
            classifier = Classifier.objects.filter(name=item.get('key').get('name'))
            Operation.objects.create(
                name=item.get('to').get('name'),
                type=item.get('to').get('type'),
                implementation=item.get('to').get('code'),
                classifier=classifier
            )
        if item.get('type') == 'new-classifier':
            Classifier.objects.create(
                name=item.get('to').get('name')
            )
    print(body_data)
    return HttpResponse('OK')

@csrf_exempt
def data(request):
    if request.method == 'POST':
        return processToBackend(request)
    else:
        classifiers = Class.objects.all()
        compositions = Composition.objects.all()
        associations = Association.objects.all()
        generalizations = Generalization.objects.all()

        nodes = dict()
        for classifier in classifiers:
            nodes[str(uuid.uuid4())] = classifierToNode(classifier)

        connections = dict()
        for composition in compositions:
            connections[str(uuid.uuid4())] = {
                'name': str(composition),
                'type': 'composition',
                'labelFrom': str(composition.multiplicity_from),
                'label': str(composition),
                'labelTo': str(composition.multiplicity_to),
                'from': getUUIDfromClassifier(
                    str(composition.classifier_from),
                    nodes
                ),
                'to': getUUIDfromClassifier(
                    str(composition.classifier_to),
                    nodes
                ),
                'id': composition.id
            }

        for association in associations:
            connections[str(uuid.uuid4())] = {
                'name': str(association),
                'type': 'association',
                'labelFrom': str(association.multiplicity_from),
                'label': str(association),
                'labelTo': str(association.multiplicity_to),
                'from': getUUIDfromClassifier(
                    str(association.classifier_from),
                    nodes
                ),
                'to': getUUIDfromClassifier(
                    str(association.classifier_to),
                    nodes
                ),
                'id': association.id
            }


        for generalization in generalizations:
            connections[str(uuid.uuid4())] = {
                'name': str(generalization),
                'type': 'generalization',
                'labelFrom': '',
                'label': str(generalization),
                'labelTo': '',
                'from': getUUIDfromClassifier(
                    str(generalization.classifier_from),
                    nodes
                ),
                'to': getUUIDfromClassifier(
                    str(generalization.classifier_to),
                    nodes
                ),
                'id': generalization.id
            }

        response = HttpResponse(str(json.dumps({
                'nodes': nodes,
                'connections': connections
            }))
        )
        response["Access-Control-Allow-Origin"] = "*"
        return response