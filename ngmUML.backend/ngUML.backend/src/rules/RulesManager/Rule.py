from .Enums import Constraints
from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError
from rules.processors.ValidatorProcessor import getStandardIfStatement, addValidator as VPaddValidator


class BaseRule:
    def __init__(self, rule_db):
        self.rule_db = rule_db
    
    @abstractmethod
    def addValidator(self):
        pass

    @abstractmethod
    def is_type(dict):
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
        if len(dict['properties']) == 1 and len(dict['classifiers']) == 1 and dict['operator'] in operators:
            return True
        else:
            return False

    def addValidator(self):
        targetProperty = self.rule_db.properties.all()[0]
        VPaddValidator(
            targetProperty, 
            self.rule_db, 
            getStandardIfStatement(
                "value " + self.rule_db.operator + " " + str(self.rule_db.value[0]), 
                self.rule_db
            )
        )


class StringRule:
    @staticmethod
    def is_type(self, dict):
        pass

    def addValidator(self):
        pass

    
    

