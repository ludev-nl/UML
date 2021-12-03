#Gegeven een lijst van lijsten, maar een database object aan
from model.models import Classifier, Property
from rules.models import Rule
from rules.RulesManager.BaseRule import BaseRule
from abc import ABC, abstractmethod

def generate_db(input):
    input_value = ""
    if(len(input['value']) != 0):
        input_value = input['value'][0]
        
    new_rule_db = Rule(
        original_input = input['original_input'],
        type = detect_type(input), 
        operator = " ".join(input['operators']), # TODO: replace [0] with a better way to handle multiple operators and values 
        value = input_value
    )

    new_rule_db.save()
    
    # Add classifiers and properties to saved rule (Needs rule to exist before foreign keys can be added)
    for classifier in input['classifiers']:
        new_rule_db.classifiers.add(classifier)
    for property in input['properties']:
        new_rule_db.properties.add(property)

    return new_rule_db

# Detect rule as dictionary of textprocessor
def detect_type(dict):
    ''' Detects the type of rule an input dictionary is.'''
    for child in BaseRule.__subclasses__():
        result = child.is_type(dict)
        if result is not False:
            return result

    raise Exception("The rule dit not conform to any implemented syntax.")

# Detect rule by database object #TODO: can this not be replaced by constructing a dictionary from the db Rule and calling detect_type? 
def generate_py_obj(rule_db):
    ''' Generates a Rule class from a DB object Rule. '''
    for child in BaseRule.__subclasses__():
        if rule_db.type == child.rule_type:
            return child(rule_db)

    else:
        raise Exception("Error: no rule class found for type" + rule_db.type)