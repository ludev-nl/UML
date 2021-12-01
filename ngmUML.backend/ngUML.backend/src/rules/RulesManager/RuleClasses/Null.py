from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator
from rules.RulesManager.BaseRule import BaseRule

#TODO: Add a generic add field thingy for a property instead of OP validator
class NullRule(BaseRule):
    """
    The syntax of the NotNullRule rule is: classifier.property "NOT NULL".
    The purpose of this rule is to enforce a property of an object to not be null or empty.
    """

    rule_type = "NULL"

    operator_keys = ["NULL"]

    text_examples = [
        "The description of an item can be empty.",
    ]

    @staticmethod
    def is_type(dict):
        if(len(dict["classifiers"])==1 and len(dict["properties"])==1 and NullRule.operator_keys[0] in dict["operators"] and len(dict["operators"]) <= 2):
            return NullRule.rule_type
        else:
            return False
    
    def get_processed_text(self):
        return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + " " + "NOT NULL"

    def add_validator(self):
        if "NOT" in self.rule_db.operator:
            add_keyword(self.rule_db.properties.all()[0], "blank", False)
        else:
            add_keyword(self.rule_db.properties.all()[0], "blank", True)

    def remove_validator(self):
        pass