from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator
from rules.RulesManager.BaseRule import BaseRule

class SymbolRule(BaseRule):
    """
    The syntax of the SymbolRule rule is: classifier.property CONTAINS # SYMBOLS.
    The purpose of this rule is to enforce the property of an object to have a limited amount of specified symbols.
    """

    rule_type = "NUM_SYMBOLS"
    
    operator_keys = ["SYMBOLS"]

    text_examples = [
        "The name of a product should consist of at most 10 symbols.",
        "Book title maximum 20 symbols."
    ]

    @staticmethod
    def is_type(dict):
        if(len(dict["classifiers"])==1 and len(dict["properties"])==1 and dict["operators"][0] in SymbolRule.operator_keys):
            return SymbolRule.rule_type
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