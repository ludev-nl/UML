from abc import abstractmethod
from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator

#WOULD BE NICE IF THERE WAS A REGULAR EXPRESSION IMPORT IN SHARED MODEL.PY
# HOW ABOUT A ADD IMPORT FUNCTION???

class BaseRule:
    def __init__(self, rule_db):
        self.rule_db = rule_db
    
    @abstractmethod
    def is_type(dict):
        pass

    @abstractmethod
    def get_validator(dict):
        pass

    @abstractmethod
    def add_validator(self):
        pass

    @abstractmethod
    def remove_validator(dict):
        pass


#TODO: Add a generic add field thingy for a property instead of OP validator
class NullRule(BaseRule):
    """
    The syntax of the NotNullRule rule is: classifier.property "NOT NULL".
    The purpose of this rule is to enforce a property of an object to not be null or empty.
    """
    @staticmethod
    def is_type(dict):
        nullOperator = "NULL"
        if(len(dict["classifiers"])==1 and len(dict["properties"])==1 and nullOperator in dict["operators"] and len(dict["operators"]) <= 2):
            return True
        else:
            return False
    
    def get_processed_text(self):
        return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + " " + "NOT NULL"

    def add_validator(self):
        if "NOT" in self.rule_db.operator:
            add_keyword(self.rule_db.properties.all()[0], "null", False)
        else:
            add_keyword(self.rule_db.properties.all()[0], "null", True)

    def remove_validator(self):
        pass

class SymbolRule(BaseRule):
    """
    The syntax of the SymbolRule rule is: classifier.property CONTAINS # SYMBOLS.
    The purpose of this rule is to enforce the property of an object to have a limited amount of specified symbols.
    """
    @staticmethod
    def is_type(dict):
        symbolOperator = ["SYMBOLS"]
        if(len(dict["classifiers"])==1 and len(dict["properties"])==1 and dict["operators"][0] in symbolOperator):
            return True
        else:
            return False
    
    def get_processed_text(self):
        return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + " " + "CONTAINS" + self.rule_db.value + " " + self.rule_db.operator

    def get_validator(self):
        return get_standard_if_statement(
            "len(value) == " + self.rule_db.value, 
            self.rule_db
        )

    def add_validator(self):
        targetProperty = self.rule_db.properties.all()[0]
        VP_add_validator(
            targetProperty, 
            self.rule_db, 
            self.get_validator()
        )
    
    def remove_validator(self):
        VP_remove_validator(self)

class ContainsOneType(BaseRule):
    """
    The syntax of the ContainsOneType rule is: classifier.property CONTAINS ONLY TYPE.
    The purpose of this rule is to enforce a property of an object to consist of one type only.
    """
    @staticmethod
    def is_type(dict):
        oneType = ["NUMBERS", "LETTERS"]
        if(len(dict["classifiers"])==1 and len(dict["properties"])==1 and len(dict["operators"]) == 1 and dict["operators"][0] in oneType):
            return True

        else:
            return False
    
    def get_processed_text(self):
        return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + " CONTAINS ONLY " + self.rule_db.operator 

    def get_validator(self):
        #TODO: Do it with regular expressions
        if(self.rule_db.operator == "LETTERS"):
            return get_standard_if_statement(
                "value.isalpha()", 
                self.rule_db
            )
        else:
            return get_standard_if_statement(
                "value.isnumeric()", 
                self.rule_db
            )

    def add_validator(self):
        targetProperty = self.rule_db.properties.all()[0]
        VP_add_validator(
            targetProperty, 
            self.rule_db, 
            self.get_validator()
        )
    
    def remove_validator(self):
        VP_remove_validator(self)

class ContainsTwoTypes(BaseRule):
    """
    The syntax of the ContainsTwoTypes rule is: classifier.property CONTAINS # TYPE1 AND # TYPE2.
    The purpose of this rule is to enforce a property to consist of two types only. 
    """
    def is_type(dict):
        twoTypes = ["NUMBERS", "LETTERS"]
        if(len(dict["classifiers"])==1 and len(dict["properties"])==1 and len(dict["operators"])==2 and dict["operators"][0] in twoTypes and dict["operators"][1] in twoTypes):
            return True
        else:
            return False
    
    def get_processed_text(self):
        return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + " CONTAINS " + self.rule_db.operator[0] + " AND " + self.rule_db.operator[1]

    def get_validator(self):
        #TODO: Do it with regular expressions
        return get_standard_if_statement(
            "not value.isalpha() and not value.isnumeric() and not len(value) == 0", 
            self.rule_db
        )

    def add_validator(self):
        targetProperty = self.rule_db.properties.all()[0]
        VP_add_validator(
            targetProperty, 
            self.rule_db, 
            self.get_validator()
        )
        pass

    def remove_validator(self):
        VP_remove_validator(self)

#TODO: If two different classes, then .save for the relationship
#TODO: Add validator for databaseObject.save() instead of just a single property 
# class PropertiesEqualValue(BaseRule):
#     """
#     The syntax of the PropertiesEqualValue rule is: classifier.property classifier.property EQUAL #.
#     The purpose of this rule is to enforce two properties of the same classifier to be equivalent to a certain value. 
#     """
#     @staticmethod
#     def is_type(dict):
#         equal = ["=="]
#         if(len(dict)["classifiers"]==1 and len(dict["properties"])==2 and dict["operators"][0] in equal):
#             return True
#         else:
#             return False
    
#     def get_processed_text(self):
#         return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[1].name + "EQUALS" + self.rule_db.value

#     def add_validator(self):
#         pass

# class NotEqual(BaseRule):
#     """
#     The syntax of the NotEqual rule is: classifier.property NOT(EQUAL) #
#     The purpose of this rule is to enforce a property of an object to not equivalent to a certain value. 
#     """
#     @staticmethod
#     def is_type(dict):
#         notEqual = ["NOT"]
#         if(len(dict["classifiers"])==1 and len(dict["properties"])==1 and dict["operators"][0] in notEqual):
#             return True
#         else:
#             return False
    
#     def get_processed_text(self):
#         return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + " " + self.rule_db.operator + " " + self.rule_db.value

#     def add_validator(self):
#         pass

class NumericalRule(BaseRule):
    """
    The syntax of the NumericalRule rule is: classifier.property operator #.
    The purpose of this rule is to enforce a property of an object to meet a certain value requirement based on the operator.
    """
    @staticmethod
    def is_type(dict):
        operators = [">", ">=", "==", "<", "<="]
        if(len(dict["classifiers"]) == 1 and len(dict["properties"]) == 1 and dict['operators'][0] in operators):
            return True
        else:
            return False

    def get_processed_text(self):
        return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + " " + self.rule_db.operator + " " + self.rule_db.value

    def get_validator(self):
        return get_standard_if_statement(
            "value " + self.rule_db.operator + " int(" + str(self.rule_db.value) + ")", 
            self.rule_db
        )

    def add_validator(self):
        targetProperty = self.rule_db.properties.all()[0]
        VP_add_validator(
            targetProperty, 
            self.rule_db, 
            self.get_validator()
        )

    def remove_validator(self):
        VP_remove_validator(self)

# Syntax from textprocessor still to put into new objects: 
"""
if re.search(searchNull,token):#not null rule
            processed_text = classifier[0] + "." + all_properties[0].name + " NOT NULL"
            break
            if re.search(searchNumSymbols, token):
                processed_text = all_classifiers[0].name + "." + all_properties[0].name + " CONTAINS" + operator + digits[0] +  " SYMBOLS"
                break
            else:
                processed_text = all_classifiers[0].name + "." + all_properties[0].name + operator + digits[0]
                break
        if (len(types)>0):#this rule contains a type specification
            if (len(digits) > 1):
                processed_text = all_classifiers[0].name + "." + all_properties[0].name + " CONTAINS " + digits[0] + " " + types[0] + " "+ digits[1] + " " + types[1]
                break
            else:
                processed_text = all_classifiers[0].name + "." + all_properties[0].name + " CONTAINS ONLY" + types[0]
                break
        if (len(all_properties) > 1):
            processed_text = all_classifiers[0].name + "." + all_properties[0].name + " " + all_classifiers[1].name + "." + all_properties[1].name + " EQUALS " + digits[0]
            break
"""
