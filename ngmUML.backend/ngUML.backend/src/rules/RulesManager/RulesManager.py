''' RulesManager manages everything rules: managing rules database,
adding new rules, finding rules, calls TextProcessor and MappingProcessor to make sure rules are correct'''
#Like: addRule(attributes...), removeRule(id), editRule(request), getAllRules(), getRule(id)
# Note: split the logic of views and the business logic of rulesmanager logically, don't just move logic from views.py to rulesmanger when there is no need for it
import json
from rules.models import Rule as RuleDB
from rules.RulesManager.BaseRule import BaseRule
from rules.RulesManager.RuleClasses import *
from rules.processors.TextProcessor import process_text


def generate_rule(input, pk):
    ''' Generates a Rule class from a DB object Rule. Takes either messy text or termlist as input'''
    # Convert string to termlist
    if isinstance(input, RuleDB):
        input = input.original_input

    if isinstance(input, str):
        input = process_text(input)


    for child in BaseRule.__subclasses__():
        if child.is_type(input):
            object = child(input, pk)
            return object

    raise Exception("Error: no rule class found for term_list generated by process_text.")


class RulesManager:
    def add_rule(messy_text):
        '''Saves the rule to the database and adds the validator. Also returns the primary key of the new rule. '''
        generate_rule(messy_text, -1) # Test if generating rule throws no errors
        new_rule_db = RuleDB(original_input = messy_text)
        new_rule_db.save()

        rule = generate_rule(messy_text, new_rule_db.pk)
        rule.add_validator()

        return new_rule_db.pk


    def remove_rule_by_pk(pk):
        """ Saves the rules. """
        rule = RuleDB.objects.get(pk=pk)
        generate_rule(rule, pk).remove_validator()
        rule.delete()

    
    def get_all_rules(self):
        ''' Returns all the rules in the database as rule objects.'''
        rules = []
        for rule in RuleDB.objects.all():
            rules.append((rule.original_input, rule.pk, generate_rule(rule.original_input, rule.pk)))

        return rules


    def get_description():
        """ Returns a dictionary with a key for every type of rule and the value is a describtive dictionary with multiple data fields."""
        description = { }
        for child in BaseRule.__subclasses__():
            # Get all operator keywords and aliases
            jsonfile = open("rules/operatorsets.json", "r")
            operator_keywords = json.load(jsonfile)
            jsonfile.close()

            # Compile all lists of operator_keys into single list
            aliases = { }
            for key in child.operator_keys:
                aliases[key] = operator_keywords[key]

            # Construct the description
            description[child.__name__] = {
                "description": ' '.join(child.__doc__.split()), # Get docstring but replace weird whitespace with single space
                "operator key": child.operator_keys,
                "operator aliases": aliases,
                "text examples": child.text_examples,
            }

        return description