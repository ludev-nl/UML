#Class that can tell if an instance of a Rule has correct references to objects in UML database
from model.models import Classifier, Property

#should return list of all data objects
def getClassifiers():
    ''' Returns all classfiers '''
    return Classifier.objects.all()

def getProperties():
    ''' Returns all properties from all classifiers '''
    return Property.objects.all()

#should return all properties of that class
def getPropertiesFromClassifierName(inputClassifier):
    ''' Returns all properties from the classfier in the parameter. Parameter is the name of the classfier. '''
    return Property.objects.filter(classifier=Classifier.objects.filter(name=inputClassifier))