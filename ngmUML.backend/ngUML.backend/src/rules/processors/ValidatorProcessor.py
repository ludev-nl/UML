from model.generators.PropertyGenerator import generate_property_declaration
import os.path

def add_validator_reference(property, rule):
    '''Adds validator reference to models.py content for (each) rule for @classifier and @property'''

    # Open and read models.py
    f = open("shared/models.py", "r")
    contents = f.readlines()

    # Search classifier and split contents into 2
    class_index = contents.index('class ' + property.classifier.name + '(models.Model):\n')
    start_contents = contents[:class_index]
    end_contents = contents[class_index:]

    # Generate property declaration and find current location of the prop
    property_declaration = generate_property_declaration(property.name, property.type)
    prop_index = end_contents.index(property_declaration)

    # Insert the validator reference into a copy of the old property
    validator_insert_pos = end_contents[prop_index].rfind(")")
    pk = rule.pk
    property_declaration = property_declaration[:validator_insert_pos] + ", validators = [rule_{pk}]".format(pk=pk) + property_declaration[validator_insert_pos:]

    # Delete previous prop, insert new one
    end_contents[prop_index] = property_declaration
    contents = "".join(start_contents) + "".join(end_contents)

    return contents

def read_validators_py():
    file_adress = "shared/validators.py" #TODO: should probably be saved somewhere else
    
    # Create validators.py if it does not already exist
    if not os.path.isfile(file_adress):
        f = open(file_adress, "w+")
        f.close()

    # Read contents
    f = open(file_adress, "r")
    contents = "".join(f.readlines())
    f.close()

    # Add import statement to validators.py if it does not already exist
    importStatement = "from django.core.exceptions import ValidationError" 
    if importStatement not in contents:
        contents = importStatement + "\n" + contents

    return contents


def add_validator_function(rule, validator):
     # Get content of validators.py as string
    contents = read_validators_py()

    # Add rule and create function
    validator_function = "\n\ndef rule_" + str(rule.pk) + "(value):\n" + validator
    if validator_function not in contents:
        contents += validator_function

    # Write to validators.py
    f = open("shared/validators.py", "w+")
    f.write("".join(contents))
    f.close()


def add_validator(property, rule, validator):
    # Add the validator between the 
    modelspy_text = add_validator_reference(property, rule)

    # Ensure that the import statement in models.py is correct
    import_statement = ( "from shared.validators import *")
    if import_statement not in modelspy_text:
        modelspyText = import_statement + "\n" + modelspy_text

    # Write the validator to validators.py
    add_validator_function(rule, validator)

    # Save text to models.py
    f = open("shared/models.py", "w")
    f.write("".join(modelspyText))
    f.close() 

def get_standard_if_statement(conditionalExpression, rule):
    return ("\tif " + conditionalExpression + ":\n"
        "\t\treturn True\n" 
        "\telse:\n" 
        "\t\traise ValidationError(\n"
        "\t\t\t'{value} does not abide by rule: '.format(value) + \'" +  rule.processed_text + "',\n"
        "\t\t\tparams={'value': value}, )\n"
        "\n\n")