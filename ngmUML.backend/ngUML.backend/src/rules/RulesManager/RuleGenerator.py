#Gegeven een lijst van lijsten, maar een database object aan
from model.models import Classifier, Property
from rules.RulesManager.Enums import Constraints
from rules.models import Rule
from rules.RulesManager.Rule import *
from abc import ABC, abstractmethod

def generate_db(input_dict):
    original_input = input_dict['original_input']
    properties = input_dict['properties']
    classifiers = input_dict['classifiers']
    operator = input_dict['operator']
    value = input_dict['value']
    type = detect_type(input_dict)

    new_rule_db = Rule(original_input = original_input, type = type.name, operator = operator, value = value)
    new_rule_db.save()
    
    for classifier in classifiers:
        new_rule_db.classifiers.add(classifier)
    for property in properties:
        new_rule_db.properties.add(property)

    return new_rule_db

def generate_py_obj(rule_db):
    if(rule_db.type == Constraints.ATTR_OP_NUM.name):
        return NumericalRule(rule_db)
    elif(rule_db.type == Constraints.ATTR_EQ_STR.name):
        return StringRule(rule_db)
    else:
        raise Exception("Error: no rule class found for type" + rule_db.type)


def detect_type(dict):
    if NumericalRule.is_type(dict):
        return Constraints.ATTR_OP_NUM
    elif StringRule.is_type(dict):
        return Constraints.ATTR_OP_STR
    raise Exception("The rule dit not confirm to any implemented syntax.")