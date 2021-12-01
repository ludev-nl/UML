from abc import abstractmethod
from rules.processors.ValidatorProcessor import add_keyword, get_standard_if_statement, add_validator as VP_add_validator, remove_validator as VP_remove_validator

class BaseRule:
    '''All rule classes should inherit from BaseRule and implement every variable and function (except for the constructor)'''
    # Every rule class should also contain a class docstring (a string literal comment at the top of the class definition such as above.)

    def __init__(self, rule_db):
        self.rule_db = rule_db

    # Identifying string, should be unique for each child class of BaseRule
    # Should be a string
    rule_type = "BASE_CLASS"

    # Any keys in this list need to match a key in operatorsets.json
    # Should be a list of strings
    operator_keys = ["OPERATOR_KEYWORD"]

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
        pass

    # Returns the rule as clear, processed (simplified) text
    # Returns a string
    @abstractmethod
    def get_processed_text(self):
        pass

    # Returns a string that contains a python function as code that validates the rule
    # Returns a string
    @abstractmethod
    def get_validator(self, dict):
        pass

    # Adds the validator to the application
    # Returns nothing
    @abstractmethod
    def add_validator(self):
        pass

    # Removes the validator from the application
    # Returns nothing
    @abstractmethod
    def remove_validator(self, dict):
        pass