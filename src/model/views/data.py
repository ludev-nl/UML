from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import *
from ..generators import *
import os
import json
import uuid

class FrontendInterface:
    def __init__(self):
        self.nodes = dict()
        self.connections = dict()
        self.changes = dict()

    def classifierOperations(self, classifier):
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

    def classifierProperties(self, classifier):
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

    def node(self, classifier):
        return {
            'type': 'Class',
            'name': str(classifier),
            'data': {
                'properties': self.classifierProperties(classifier),
                'methods': self.classifierOperations(classifier)
            },
            'instances': {},
            'id': classifier.id
        }

    def connection(self, relation, relation_type):
        if relation_type == 'generalization':
            m_from = ''
            m_to = ''
        else:
            m_from = relation.multiplicity_from
            m_to = relation.multiplicity_to
        return dict({
            str(uuid.uuid4()): {
                'name': str(relation),
                'type': relation_type,
                'labelFrom': str(m_from),
                'label': str(relation),
                'labelTo': str(m_to),
                'from': self.nodeUUID(
                    str(relation.classifier_from)
                ),
                'to': self.nodeUUID(
                    str(relation.classifier_to)
                ),
                'id': relation.id
            }
        })
    
    def populateNodes(self):
        for classifier in Classifier.objects.all():
            self.nodes[str(uuid.uuid4())] = self.node(classifier)
    
    def nodeUUID(self, name):
        for key, value in self.nodes.items():
            if value.get('name') == name:
                return key
        return ''

    def populateConnections(self):
        compositions = Composition.objects.all()
        associations = Association.objects.all()
        generalizations = Generalization.objects.all()

        for relation in compositions:
            self.connections = {
                **self.connections,
                **self.connection(relation, 'composition')
            }

        for relation in associations:
            self.connections = {
                **self.connections,
                **self.connection(relation, 'association')
            }

        for relation in generalizations:
            self.connections = {
                **self.connections,
                **self.connection(relation, 'generalization')
            }

    def request(self):
        self.populateNodes()
        self.populateConnections()
        response = HttpResponse(str(json.dumps({
                'nodes': self.nodes,
                'connections': self.connections
            }))
        )
        response["Access-Control-Allow-Origin"] = "*"
        return response

    def delete(self, obj_type, pk):
        if obj_type == 'property' or obj_type == 'method':
            p = Property.objects.get(id=pk)
            print(p)
            PropertyGenerator(p).delete(False)
            p.delete()
        if obj_type == 'connection':
            r = Relationship.objects.get(id=pk)
            r.delete()
        if obj_type == 'classifier':
            c = Classifier.objects.get(id=pk)
            ClassifierGenerator(c).delete(False)
            c.delete()

    def new(self, obj_type, obj):
        print(obj_type)
        print(obj)

    def push(self, request):
        body_unicode = request.body.decode('utf-8')
        self.changes = json.loads(body_unicode)
        for item in self.changes:
            action = item.get('type')
            if action.startswith('delete'):
                self.delete(
                    action.split('-')[1],
                    item.get('to').get('id')
                )
        return HttpResponse('OK')


'''
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
        if item.get('type') == 'connection-cardinality-from':
            if item.get('from').get('type') == 'association':
                pk = item.get('from').get('id')
                association = Association.objects.filter(
                    id=pk
                )
                association.multiplicity_from = item.get('to')
                association.save()
        if item.get('type') == 'connection-cardinality-to':
            if item.get('from').get('type') == 'association':
                pk = item.get('from').get('id')
                association = Association.objects.filter(
                    id=pk
                )
                association.multiplicity_to = item.get('to')
                association.save()
    print(body_data)
    return HttpResponse('OK')
'''

@csrf_exempt
def data(request):
    frontend_interface = FrontendInterface()
    if request.method == 'POST':
        return frontend_interface.push(request)
    else:
        return frontend_interface.request()