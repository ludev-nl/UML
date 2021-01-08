from django.shortcuts import render
from django.shortcuts import redirect
from ..models import Classifier, Relationship, Association, Generalization
from ..generators import *


def index(request):
    relationships = Relationship.objects.all()
    for relationship in relationships:
        relationship.name = relationship.__str__()
    context = {
        'relationships': relationships
    }

    return render(request, 'relationships.html', context)


def add(request):
    if request.method == 'GET':
        types = __get_deepest_subclasses(Relationship)
        classifiers = Classifier.objects.all()
        context = {
            'types': types,
            'classifiers': classifiers,
        }

        return render(request, 'add_relationship.html', context)

    classifier_from = Classifier.objects.get(id=request.POST['classifier_from'])
    classifier_to = Classifier.objects.get(id=request.POST['classifier_to'])
    multiplicity_from = request.POST['multiplicity_from']
    multiplicity_to = request.POST['multiplicity_to']
    name = request.POST['name']
    relationship_type = request.POST['type']

    if relationship_type == 'Association':
        relationship = Association(
            classifier_from=classifier_from,
            classifier_to=classifier_to,
            multiplicity_from=multiplicity_from,
            multiplicity_to=multiplicity_to,
            name=name)
        relationship.save()
    elif relationship_type == 'Generalization':
        relationship = Generalization()
        relationship.save()

    return redirect('/model/relationships')


def add_generalization(request):
    if request.method == 'GET':
        classifiers = Classifier.objects.all()
        context = {
            'classifiers': classifiers,
        }

        return render(request, 'add_generalization.html', context)

    classifier_from = Classifier.objects.get(id=request.POST['classifier_from'])
    classifier_to = Classifier.objects.get(id=request.POST['classifier_to'])
    generalization = Generalization(classifier_from=classifier_from, classifier_to=classifier_to)
    generalization.save()
    return redirect('/model/relationships')


def add_association(request):
    if request.method == 'GET':
        classifiers = Classifier.objects.all()
        context = {
            'classifiers': classifiers,
        }

        return render(request, 'add_association.html', context)

    classifier_from = Classifier.objects.get(id=request.POST['classifier_from'])
    classifier_to = Classifier.objects.get(id=request.POST['classifier_to'])
    multiplicity_from = request.POST['multiplicity_from']
    multiplicity_to = request.POST['multiplicity_to']
    name = request.POST['name']
    end_from = request.POST['end_from']
    end_to = request.POST['end_to']

    association = Association(
        classifier_from=classifier_from,
        classifier_to=classifier_to,
        multiplicity_from=multiplicity_from,
        multiplicity_to=multiplicity_to,
        name=name,
        end_from=end_from,
        end_to=end_to)

    RelationshipGenerator(association).generate()
    association.save()
    return redirect('/model/relationships')


def delete(request, relationship_id):
    relationship = Relationship.objects.get(id=relationship_id)
    relationship.delete()
    return redirect('/model/relationships')


def __get_deepest_subclasses(subclass):
    classes = []
    for cls in subclass.__subclasses__():
        if cls.__subclasses__():
            for scls in __get_deepest_subclasses(cls):
                classes.append(scls)
        else:
            classes.append(cls.__name__)

    return classes
