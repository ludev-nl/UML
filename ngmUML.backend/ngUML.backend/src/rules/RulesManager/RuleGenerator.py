#Gegeven een lijst van lijsten, maar een database object aan
from model.models import Classifier, Property
from rules.RulesManager.Enums import Constraints
from rules.models import Rule
from abc import ABC, abstractmethod
from rules.processors.ValidatorProcessor import getStandardIfStatement, addValidator as VPaddValidator
from django.core.exceptions import ValidationError

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

#rules

class BaseRule:
    def __init__(self, rule_db):
        self.rule_db = rule_db
    
    @abstractmethod
    def addValidator(self):
        pass

    @abstractmethod
    def is_type(dict):
        pass

class NumericalRule(BaseRule):
    

    @staticmethod
    def is_type(dict):
        operators = [
        ">",
        ">=",
        "==",
        "<",
        "<="
        ]
        if len(dict['properties']) == 1 and len(dict['classifiers']) == 1 and dict['operator'] in operators:
            return True
        else:
            return False

    def addValidator(self):
        targetProperty = self.rule_db.properties.all()[0]
        VPaddValidator(
            targetProperty, 
            self.rule_db, 
            getStandardIfStatement(
                "value " + self.rule_db.operator + " " + str(self.rule_db.value[0]), 
                self.rule_db
            )
        )

class StringRule:
    @staticmethod
    def is_type(self, dict):
        pass

    def addValidator(self):
        pass

    
    