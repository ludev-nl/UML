from abc import abstractmethod
from rules.RulesManager.TermList import TermList
from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator
from rules.processors.ModelPaths import get_pathing_from_classifier, get_possible_classifiers
from rules.RulesManager.BaseRule import BaseRule
from rules.RulesManager.Terms  import Operator, Value
from model.models import Class, Classifier, Property

class RelationshipRule(BaseRule):
    ''' Relationship rule allows the user to make a rule about a property and the property of a linked object'''

    operator_keys = [">", ">=", "==", "<", "<="]

    # A couple of examples of text input for this rule
    # Should be a list of strings
    text_examples = [
        "Example rule 1",
        "Example rule 2"
    ]

    # Should test if an incoming rule dictionary fits the syntax of the rule
    # Returns rule_type or False
    @abstractmethod
    def is_type(termlist):
        return termlist.count(2, 2, 1, 0) and termlist[Operator, 0] in RelationshipRule.operator_keys

    # Returns the rule as clear, processed (simplified) text
    # Returns a string
    @abstractmethod
    def get_processed_text(self):
        return self.termlist[Classifier, 0].name + self.termlist[Property, 0].name + self.termlist[Operator, 0] + self.termlist[Classifier, 1].name + self.termlist[Property, 1].name 

    # Returns a string that contains a python function as code that validates the rule
    # Returns a string
    @abstractmethod
    def get_validator(self, termlist):
        classifier = self.termlist[Classifier, 0]
        print(get_pathing_from_classifier(classifier)) # Call to get path in graph

    # Adds the validator to the application
    # Returns nothing
    @abstractmethod
    def add_validator(self):
        self.get_validator(self.termilst)

    # Removes the validator from the application
    # Returns nothing
    @abstractmethod
    def remove_validator(self, dict):
        pass