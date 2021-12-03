from abc import abstractmethod
from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator
from rules.processors.ModelPaths import get_pathing_from_classifier, get_possible_classifiers
from rules.RulesManager.BaseRule import BaseRule

class RelationshipRule(BaseRule):
    ''' Relationship rule allows the user to make a rule about a property and the property of a linked object'''

    rule_type = "RELATIONSHIP"

    operator_keys = ["RELATIONSHIP"]

    # A couple of examples of text input for this rule
    # Should be a list of strings
    text_examples = [
        "Example rule 1",
        "Example rule 2"
    ]

    # Should test if an incoming rule dictionary fits the syntax of the rule
    # Returns rule_type or False
    @abstractmethod
    def is_type(dict):
        if len(dict["classifiers"]) == 2 and len(dict["properties"]) == 2 and dict["operators"][0] in RelationshipRule.operator_keys:
            return RelationshipRule.rule_type
        else:
            return False

    # Returns the rule as clear, processed (simplified) text
    # Returns a string
    @abstractmethod
    def get_processed_text(self):
        return "IMPLEMENT"

    # Returns a string that contains a python function as code that validates the rule
    # Returns a string
    @abstractmethod
    def get_validator(self, dict):
        classifier = dict.classifiers.all()[0]
        print(get_pathing_from_classifier(classifier)) # Call to get path in graph

    # Adds the validator to the application
    # Returns nothing
    @abstractmethod
    def add_validator(self):
        self.get_validator(self.rule_db)

    # Removes the validator from the application
    # Returns nothing
    @abstractmethod
    def remove_validator(self, dict):
        pass