''' RulesManager manages everything rules: managing rules database,
adding new rules, finding rules, calls TextProcessor and MappingProcessor to make sure rules are correct'''
#Like: addRule(attributes...), removeRule(id), editRule(request), getAllRules(), getRule(id)
# Note: split the logic of views and the business logic of rulesmanager logically, don't just move logic from views.py to rulesmanger when there is no need for it
from ..models import Rule as RuleDB
from ssl import create_default_context
from rules.RulesManager.Rule import numericalRule
from rules.processors.TextProcessor import determine_rule_type, process_text
from rules.RulesManager.Enums import Constraints

class RulesManager:
    def __init__(self):
        self.factory = RulesFactory()

    #database functions start with db_
    def db_add_rule(self, messy_text):
        '''Tries to save rule to the database. No exceptions are caught yet.
        Uses text processer to map messy text to processed text,
        and determine what type of processed text maps to'''
        processed_text = process_text(messy_text)
        detected_constraint = determine_rule_type(processed_text)
        new_rule = self.factory.create_rule(detected_constraint, processed_text)
        python_string = new_rule.get_as_python()
        db_rule = RuleDB(messy_rule = messy_text, processed_rule = processed_text, type = detected_constraint.value, python = python_string)
        db_rule.save()

    def db_get_all_rules(self):
        return RuleDB.objects.all()

    def db_get_rule_by_id(self, id):
        return RuleDB.objects.get(pk=id)

    #rule class instance functions
    def get_all_rules(self):
        query = RuleDB.objects.all()
        list = []
        for db_rule in query:
            list.append(self.factory.create_rule(Constraints[db_rule.type], db_rule.processed_rule))
        return list

    def get_rule_by_id(self, id):
        db_rule = RuleDB.objects.get(pk=id)
        self.factory.create_rule(db_rule.type, db_rule.processed_text)



class RulesFactory:
    def create_rule(self, type, text_rule):
        '''Returns instance of subclass of given rule type with textrule
        For now: Only call this if you know that text_rule can be safely passed to constructor
        of that type.'''
        if(type == Constraints.ATTR_OP_NUM):
            return numericalRule(text_rule)
        elif(type == Constraints.MAX_SYMBOL):
            return maxSymbolRule(text_rule)
        elif(type == Constraints.SPECIFIC_CHAR):
            return specificCharacterTypeRule(text_rule)
        elif(type == Constraints.ORDER_CHAR):
            return characterOrderRule(text_rule)
        elif(type == Constraints.NULL):
            return nullRule(text_rule)
        elif(type == Constraints.ATTRIBUTES_EQ_NUM):
            return attributesEqualValueRule(text_rule)
        else:
            raise Exception("Error: can't create rule of type: " + type)
