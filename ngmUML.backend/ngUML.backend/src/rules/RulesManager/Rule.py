import shlex #for splitting on spaces but preserving quotation marks
from .Enums import Constraints
from abc import ABC, abstractmethod

class Rule:
    @abstractmethod
    def __init__(self, text_rule):

        
        ''' Constructor function'''
        # Rule for now is a string with a strict structure: 
        # "<classifier> <attribute> <condition> <value>"

        # Example:
        # "Warehouse storagecapacity atleast 50"
        self.text_rule = text_rule

    @abstractmethod
    def check_rule(rule_text):
        ''' Returns if the representation produced by TextProcessor can be converted to the rule'''
        pass
        
    def get_as_dict(self):
        ''' Returns the rule as a dictionary (JSON) with all individual properties as keys.'''
        return self.components

    def get_as_text(self):
        ''' Returns the entire rule as text '''
        return self.text_rule

    #this depends on the kind of rule
    @abstractmethod
    def get_as_python(self):
        pass


class numericalRule(Rule):
    def __init__(self, text_rule):
        self.text_rule = text_rule
        split = text_rule.split()
        self.components = {
            "classifier": split[0],
            "attribute": split[1],
            "operator": split[2],
            "value": split[3],
        }

    @staticmethod
    def check_rule(text):
        operators = [">", ">=", "=", "<", "<="]
        verify_components = text.lower().split()
        if(len(verify_components) != 4):
            print("error amount of arguments should be 4, is " + str(len(verify_components)))
            return False
        if(verify_components[2] not in operators):
            print("error no boolean operator: should be one of '>, <, <=, >=, =', is: " + verify_components[2])
            return False
        if(not verify_components[3].isdecimal()):
            print("Error no numeric value")
            return False
        return True
        
    def get_as_python(self):
        return "if(" + self.components["classifier"] + "." + self.components["attribute"] + self.components["operator"] + self.components["value"] + ")"
    pass

class stringRule(Rule):
    def __init__(self, text_rule):
        self.text_rule = text_rule
        split = shlex.split(text_rule)
        self.components = {
            "classifier": split[0],
            "attribute": split[1],
            "equals": split[2],
            "string": split[3],
        }

    @staticmethod
    def check_rule(text):
        operators = ["==", "!=",]
        verify_components = shlex.split(text.lower())
        if(len(verify_components) != 4):
            print("error amount of arguments should be 4, is " + str(len(verify_components)))
            return False
        if(verify_components[2] not in operators):
            print("error no boolean operator: should be one of '==, !=', is: " + verify_components[2])
            return False
        return True

    def get_as_python(self):
        return "if(" + self.components["classifier"] + "." + self.components["attribute"] + self.components["equals"] + self.components["string"] + ")"
    pass




        

