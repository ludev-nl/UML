from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator
from rules.RulesManager.BaseRule import BaseRule

class ContainsOneType(BaseRule):
    """
    The syntax of the ContainsOneType rule is: classifier.property CONTAINS ONLY TYPE.
    The purpose of this rule is to enforce a property of an object to consist of one type only.
    """
    
    rule_type = "ONE_TYPE"
    
    operator_keys = ["NUMBERS", "LETTERS"]

    text_examples = [
        "The name of a city only contains letters.",
        "A serical code of a product only contains numbers.",
    ]

    @staticmethod
    def is_type(dict):
        if(len(dict["classifiers"])==1 and len(dict["properties"])==1 and len(dict["operators"]) == 1 and dict["operators"][0] in ContainsOneType.operator_keys):
            return ContainsOneType.rule_type
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