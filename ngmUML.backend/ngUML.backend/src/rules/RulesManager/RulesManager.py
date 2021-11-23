''' RulesManager manages everything rules: managing rules database,
adding new rules, finding rules, calls TextProcessor and MappingProcessor to make sure rules are correct'''
#Like: addRule(attributes...), removeRule(id), editRule(request), getAllRules(), getRule(id)
# Note: split the logic of views and the business logic of rulesmanager logically, don't just move logic from views.py to rulesmanger when there is no need for it
from ..models import Rule as RuleDB
from ssl import create_default_context
from rules.processors.TextProcessor import process_text
from rules.RulesManager.Enums import Constraints
import rules.RulesManager.RuleGenerator as RuleGenerator
from model.models import Classifier, Property

class RulesManager:
    #database functions start with db_
    def db_add_rule(self, messy_text):
        '''Tries to save rule to the database. No exceptions are caught yet.
        Uses text processer to map messy text to processed text,
        and determine what type of processed text maps to'''
        processed_dict = process_text(messy_text)   
        new_rule_db = RuleGenerator.generate_db(processed_dict)
        new_rule = RuleGenerator.generate_py_obj(new_rule_db)
        new_rule_db.processed_text = new_rule.get_processed_text()
        new_rule_db.save()
        new_rule.add_validator()

    def db_remove_rule_by_pk(self, pk):
        rule = RuleDB.objects.get(pk=pk)
        RuleGenerator.generate_py_obj(rule).remove_validator()
        rule.delete()

    
    def db_get_all_rules(self):
        return RuleDB.objects.all()

    def db_get_rule_by_pk(self, pk):
        return RuleDB.objects.get(pk=pk)

    #rule class instance functions
    def get_all_rules(self):
        query = RuleDB.objects.all()
        list = []
        for db_rule in query:
            list.append(self.factory.create_rule(Constraints[db_rule.type], db_rule.processed_rule))
        return list

    def get_rule_by_pk(self, pk):
        db_rule = RuleDB.objects.get(pk=pk)
        #TODO: also set the pk of the rule, for valikator 
        self.factory.create_rule(db_rule.type, db_rule.processed_text)
