from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator
from rules.RulesManager.BaseRule import BaseRule

class ContainsTwoTypes(BaseRule):
    """
    The syntax of the ContainsTwoTypes rule is: classifier.property CONTAINS # TYPE1 AND # TYPE2.
    The purpose of this rule is to enforce a property to consist of two types only. 
    """
    
    rule_type = "TWO_TYPES"
        
    operator_keys = ["NUMBERS", "LETTERS"]

    text_examples = [
        "A zipcode of an adress should only consist of numbers and letters."
    ]

    @staticmethod
    def is_type(dict):
        if(len(dict["classifiers"])==1 and len(dict["properties"])==1 and len(dict["operators"])==2 and dict["operators"][0] in ContainsTwoTypes.operator_keys and dict["operators"][1] in ContainsTwoTypes.operator_keys):
            return ContainsTwoTypes.rule_type
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