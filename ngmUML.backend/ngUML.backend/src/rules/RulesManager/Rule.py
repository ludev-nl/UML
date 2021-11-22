from abc import abstractmethod
from rules.processors.ValidatorProcessor import get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator


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
        if len(dict['properties']) == 1 and len(dict['classifiers']) == 1 and dict['operators'][0] in operators:
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

class StringRule:
    @staticmethod
    def is_type(dict):
        pass

    def add_validator(self):
        pass


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
    
    

#hieronder