#Class that can tell if an instance of a Rule has correct references to objects in UML database
from model.models import Classifier, Property

def getClassifiers():
    ''' Returns all classfiers '''
    names = list()
    for classifier in Classifier.objects.all():
        names.append(classifier.name)

    return names


def getProperties():
    ''' Returns all properties from all classifiers '''
    names = list()
    for property in Property.objects.all():
        names.append(property.name)

    return names


def getPropertiesFromClassifiers(inputClassifier):
    ''' Returns all properties from the classfier in the parameter. Parameter is the name of the classfier. '''
    names = list()
    for property in Property.objects.filter(classifier=Classifier.objects.filter(name=inputClassifier)):
        names.append(property.name)

    return names