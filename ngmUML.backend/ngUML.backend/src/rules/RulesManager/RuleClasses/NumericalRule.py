from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator
from rules.RulesManager.BaseRule import BaseRule

class NumericalRule(BaseRule):
    """
    The syntax of the NumericalRule rule is: classifier.property operator #.
    The purpose of this rule is to enforce a property of an object to meet a certain value requirement based on the operator.
    """

    rule_type = "NUMERICAL_SINGULAR_PROP"

    operator_keys = [">", ">=", "==", "<", "<="]

    text_examples = [
        "Product price > 0",
        "Elevator load should be at most 5000 kg.",
        "Team size should be at least two members.",
        "The capacity of a small delivery truck is equal to 1000 kgs."
    ]

    @staticmethod
    def is_type(dict):
        if(len(dict["classifiers"]) == 1 and len(dict["properties"]) == 1 and dict['operators'][0] in NumericalRule.operator_keys):
            return NumericalRule.rule_type
        else:
            return False

    def get_processed_text(self):
        return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + " " + self.rule_db.operator + " " + self.rule_db.value

    def get_validator(self):
        return get_standard_if_statement(
            "int(value) " + self.rule_db.operator + " " + str(self.rule_db.value), 
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
