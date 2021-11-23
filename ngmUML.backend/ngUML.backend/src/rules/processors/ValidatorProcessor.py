from model.generators.PropertyGenerator import generate_property_declaration
import os.path

def read_from_shared_file(name):
    f = open("shared/" + name + ".py", "r")
    text = f.read()
    f.close()

    return text


def write_to_shared_file(name, text):
    f = open("shared/" + name + ".py", "w+")
    f.write(text)
    f.close()


def get_validator_function_reference(rule):
    return "rule_" + str(rule.pk)


def get_validator_function_definition(rule, validator):
    return "\n\ndef rule_" + str(rule.pk) + "(value):\n" + validator


def add_validator_reference(property, rule):
    '''Adds validator reference to models.py text for (each) rule for @classifier and @property'''

    # Open and read models.py
    text = read_from_shared_file("models")

    # Ensure that the import statement in models.py is correct
    import_statement = ( "from shared.validators import *\n")
    if import_statement not in text:
        text = import_statement + text

    # Search classifier and split text into 2
    class_string = 'class ' + property.classifier.name + '(models.Model):\n'
    class_index = text.find(class_string) + len(class_string)
    base_text = text[:class_index]
    classifier_text = text[class_index:]

    # Generate property declaration and find index of the beginning and the end of the prop in text
    old_property = generate_property_declaration(property.name, property.type)[:-2]
    property_index = classifier_text.find(old_property) + len(old_property)
    target_text = classifier_text[property_index:]
    classifier_text = classifier_text[:property_index]
    end_of_property_index = target_text.find('\n')

    # Add the reference
    reference = get_validator_function_reference(rule) + ", ]"
    if "validators" in target_text[:end_of_property_index]:
        target_text = target_text.replace(" ]", " " + reference, 1)
    else:
        target_text = target_text.replace(")", ", validators = [" + reference + ")", 1)

    # Save text to models.py
    write_to_shared_file("models", base_text + classifier_text + target_text)


def read_validators_py():
    # Create validators.py if it does not already exist
    if not os.path.isfile("shared/validators.py"):
        write_to_shared_file("validators", "")

    # Read texts
    text = read_from_shared_file("validators")

    # Add import statement to validators.py if it does not already exist
    import_statement = "from django.core.exceptions import ValidationError" 
    if import_statement not in text:
        text = import_statement + "\n" + text

    return text


def add_import_statement(import_statement):
    text = read_validators_py()

    if import_statement not in text:
        text = import_statement + "\n" + text
    
    write_to_shared_file("validators", text)


def add_validator_function(rule, validator):
    text = read_validators_py()

    # Add rule and create function
    validator_function = get_validator_function_definition(rule, validator)
    if validator_function not in text:
        text += validator_function

    write_to_shared_file("validators", text)


def add_validator(property, rule, validator):
    add_validator_reference(property, rule)
    add_validator_function(rule, validator)


def remove_validator_reference(rule):
    ''' Removes "rule_pk" from models.py '''
    text = read_from_shared_file("models")
    text = text.replace(get_validator_function_reference(rule.rule_db) + ", ", '', 1)
    write_to_shared_file("models", text)


def remove_validator_function(rule):
    text = read_from_shared_file("validators")
    validator_function = get_validator_function_definition(rule.rule_db, rule.get_validator())
    print(validator_function)
    text = text.replace(validator_function, '')
    write_to_shared_file("validators", text)


def remove_validator(rule):
    remove_validator_reference(rule)
    remove_validator_function(rule)


def get_standard_if_statement(conditionalExpression, rule):
    return ("\tif " + conditionalExpression + ":\n"
        "\t\treturn True\n" 
        "\telse:\n" 
        "\t\traise ValidationError(\n"
        "\t\t\t'{value} does not abide by rule: '.format(value) + \'" +  rule.processed_text + "',\n"
        "\t\t\tparams={'value': value}, )\n")