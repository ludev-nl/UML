from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator
from rules.processors.ValidatorProcessor import get_standard_if_statement_spaces, add_to_method_in_classifier as VP_add_to_method_in_classifier
from rules.RulesManager.BaseRule import BaseRule

class NumericalTwoProperties(BaseRule):
    """
    The syntax of the NumericalTwoProperties rule is: classifier.property operator classifier.property.
    The purpose of this rule is to enforce two properties of an object to meet a certain numerical relation based on the operator.
    """

    rule_type = "NUMERICAL_TWO_PROP"

    operator_keys = [">", ">=", "==", "<", "<="]

    text_examples = [
        "Elevator load <= Elevator capacity",
        "The number of doors in a house must be at least equal to the number of rooms",
        "Team size should be at least minimumTeamSize",
    ]

    @staticmethod
    def is_type(dict):
        if(len(dict["classifiers"]) == 1 and len(dict["properties"]) == 2 and dict['operators'][0] in NumericalTwoProperties.operator_keys):
            return NumericalTwoProperties.rule_type
        else:
            return False

    def get_processed_text(self):
        return self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[0].name + " " + self.rule_db.operator + " " + self.rule_db.classifiers.all()[0].name + "." + self.rule_db.properties.all()[1].name

    def get_validator(self):
        return get_standard_if_statement_spaces(
            str("self." + self.rule_db.properties.all()[0].name) + str(self.rule_db.operator) + " self." + str(self.rule_db.properties.all()[1]), 
            self.rule_db
        )

    def add_validator(self):
        targetClassifier = self.rule_db.classifiers.all()[0]
        targetMethod = "def clean(self):"
        VP_add_to_method_in_classifier(
            targetClassifier,
            targetMethod,
            self.get_validator()
        )
    def remove_validator(self):
        pass
