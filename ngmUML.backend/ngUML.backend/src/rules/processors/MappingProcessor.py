#Class that can tell if an instance of a Rule has correct references to objects in UML database
from model.models import Classifier, Property

def getClassifiers():
    names = list()
    for classifier in Classifier.objects.all():
        names.append(classifier.name)

    return names

def getProperties():
    names = list()
    for property in Property.objects.all():
        names.append(property.name)

    return names