import shlex #for splitting on spaces but preserving quotation marks
from .Enums import Constraints
from abc import ABC, abstractmethod

#TODO: Add id field
class Rule:
    @abstractmethod
    def __init__(self, text_rule):


        ''' Constructor function'''
        # Rule for now is a string with a strict structure:
        # "<classifier> <property> <condition> <value>"

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
            "property": split[1],
            "operator": split[2],
            "value": split[3]
        }

    @staticmethod
    def check_rule(text):
        # OBJECT PROPERTY OPERATOR VALUE
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
    
    #CONTEXT: In the generated application, in models.py
    #the rule should be added to the list of validators for the relevant field in the model
    # so if string total should not exceed 100 in the model Order, then in models.py do:
    # class Order(models.Model):
    #   total = models.IntegerField(validators=[%FindRule.getRuleFunctionName()];
    # Example of generated function for numericalRule:
    # """def rule_[id](inputvalue_of_field):
    #     if inputvalue_of_field [operator] [number]:
    #         raise ValidationError(
    #             '%(inputvalue_of_field)s is not %([operator])s %([number]s) 
    #              params={'value': inputvalue_of_field)}) """
    #         
    # from django.core.exceptions import ValidationError
    #    this should be put in the file where the function is inserted

    # returns validator as function (string)
    def get_as_validator(self):
        pass
    pass

class stringRule(Rule):
    def __init__(self, text_rule):
        self.text_rule = text_rule
        split = shlex.split(text_rule)
        self.components = {
            "classifier": split[0],
            "property": split[1],
            "operator": split[2],
            "value": split[3]
        }
    @staticmethod
    def check_rule(text):
        # [OBJECT.PROPERTY] CONTAINS [OPERATOR] # SYMBOLS
        operators = ["==", "!=",">", ">=", "=", "<", "<="]
        verify_components = shlex.split(text.lower())
        if(len(verify_components) != 5):
            print("error amount of arguments should be 4, is " + str(len(verify_components)))
            return False
        if(verify_components[2] not in operators):
            print("error no boolean operator: should be one of '==, !=', '>', '>=', '=', '<', '<=', is: " + verify_components[2])
            return False
        return True

    def get_as_python(self):
        return "if(" + self.components["classifier"] + "." + self.components["property"] + self.components["operator"] + self.components["value"] + ")"
    pass

class specificCharacterTypeRule(Rule):
    def __init__(self, text_rule):
        self.text_rule = text_rule
        split = shlex.split(text_rule)
        self.components = {
            "classifier": split[0],
            "property": split[1],
            "type": split[-1]
        }
        @staticmethod
        def check_rule(text):
            # OBJECT PROPERTY 'numbers/letters'
            verify_components = shlex.split(text.lower())
            if(len(verify_components) != 3):
                print("error amount of arguments should be 3, is " + str(len(verify_components)))
                return False
            if(verify_components[2] != 'numbers' and verify_components[2] != 'letters'):
                print("argument should be numbers or letters and is" + verify_components[2])
                return False

        def get_as_python(self):
            if (verify_components[2] == 'numbers'):
                return "if(" + self.components["classifier"] + "." + self.components["property"] + ".isnumeric()"")"
            if (verify_components[2] == 'letters'):
                return "if(" + self.components["classifier"] + "." + self.components["property"] + ".isalpha()"")"
        return True

class characterOrderRule(Rule):
    def __init__(self, text_rule):
        self.text_rule = text_rule
        split = shlex.split(text_rule)
        self.components = {
            "classifier": split[0],
            "property": split[1],
            "value1": split[2],
            "type1": split[3],
            "value2": split[4],
            "type2": split[5]
        }
    @staticmethod
    def check_rule(text):
        # OBJECT PROPERTY NUMBER 'numbers/letters' NUMBER 'number/letters'
        verify_components = shlex.split(text.lower())
        if(len(verify_components) != 6):
            print("error amount of arguments should be 6, is " + str(len(verify_components)))
            return False
        if((verify_components[3] != 'numbers' and verify_components[3] != 'letters')
           and (verify_components[5] != 'numbers' and verify_components[5] != 'letters')):
            print("argument should be numbers or letters and is" + verify_components[2])
            return False
        if((verify_components[2].isnumeric() and verify_components[4].isnumeric())):
            if(int(verify_components[2])<1 or int(verify_components[4])<1):
                print("arguments 2 and 4 should be at least 1 and are" + verify_components[2] + ' ' + verify_components[4])
                return False
        else:
            print("arguments 2 and 4 should be numbers and are " + verify_components[2] + ' ' + verify_components[4])
            return False
        return True

    def get_as_python(self):
        if (verify_components[2] == 'numbers' and verify_components[4] == 'numbers'):
            return "if(" + self.components["classifier"] + "." + self.components["property"] + ".isnumeric()"")"
        elif (verify_components[2] == 'letters' and verify_components[4] == 'letters'):
            return "if(" + self.components["classifier"] + "." + self.components["property"] + ".isalpha()"")"
        elif (verify_components[2] == 'letters' and verify_components[4] == 'numbers'):
            return "if(" + self.components["classifier"] + "." + self.components["property"] + "[0:" + int(self.components["value1"])-1 + "]" + ".isalpha() and"+ self.components["classifier"] + "." + self.components["property"] + "[" + int(self.components["value1"]) + ":" + int(self.components["value1"])+int(self.components["value2"])-1 + ".isnumeric()" + ")"
        elif (verify_components[2] == 'numbers' and verify_components[4] == 'letters'):
            return "if(" + self.components["classifier"] + "." + self.components["property"] + "[0:" + int(self.components["value1"])-1 + "]" + ".isnumeric() and" + self.components["classifier"] + "." + self.components["property"] + "[" + int(self.components["value1"]) + ":" + int(self.components["value1"])+int(self.components["value2"])-1 + ".isalpha()" + ")"
        pass

    class nullRule(Rule):
        def __init__(self, text_rule):
            self.text_rule = text_rule
            split = shlex.split(text_rule)
            self.components = {
                "classifier": split[0],
                "property": split[1]
            }
        @staticmethod
        def check_rule(text):
            # OBJECT PROPERTY NOT NULL
            verify_components = shlex.split(text.lower())
            if(len(verify_components) != 4):
                print("error amount of arguments should be 4, is " + str(len(verify_components)))
                return False
            return True

        def get_as_python(self):
            return "if(" + self.components["classifier"] + "." + self.components["property"] + "is not ''" + ")"

    class propertiesEqualValueRule(Rule):
        def __init__(self, text_rule):
            self.text_rule = text_rule
            split = shlex.split(text_rule)
            self.components = {
                "classifier1": split[0],
                "property1": split[1],
                "classifier2": split[2],
                "property2": split[3],
                "value": split[4]
            }
        @staticmethod
        def check_rule(text):
            #OBJECT PROPERTY1 OBJECT PROPERTY2 NUMBER
            verify_components = shlex.split(text.lower())
            if(len(verify_components) != 5):
                print("error amount of arguments should be 5, is " + str(len(verify_components)))
                return False
            if(not verify_components[4].isnumeric()):
                print("argument should be a number and is " + verify_components[4])
                return False
            return True

        def get_as_python(self):
            return "if(" + self.components["classifier1"] + "." + self.components["property1"] + " " + self.components["classifier2"] + "." + self.components["property2"] + " == " + self.components["value"] + ")"
    # class defaultNumberRule(Rule):
    #     def __init__(self, text_rule):
    #         self.text_rule = text_rule
    #         split = shlex.split(text_rule)
    #         self.components = {
    #             "classifier": split[0],
    #             "attribute": split[1],
    #             "value": split[2]
    #         }
    #     def check_rule(text):
    #         # OBJECT ATTRIBUTE NUMBER
    #         verify_components = shlex.split(text.lower())
    #         if(len(verify_components) != 3):
    #             print("error amount of arguments should be 6, is " + str(len(verify_components)))
    #             return False
    #         if(not verify_components[2].isnumeric()):
    #             print("argument should be a number and is " + verify_components[2])
    #             return False
    #         return True
    #
    # TODO: def get_as_python(self):
