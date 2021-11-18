from model.generators.PropertyGenerator import generate_property_declaration
import os.path

def addValidatorReference(property, rule):
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

def addValidatorFunction(rule, validator):
    file_adress = "shared/validators.py"
    
    if not os.path.isfile(file_adress):
        f = open(file_adress, "w+")
        f.close()

    f = open(file_adress, "r")
    contents = f.readlines()
    contents = "".join(contents)
    f.close()

    importStatement = "from django.core.exceptions import ValidationError" 
    if importStatement not in contents:
        contents = importStatement + "\n" + contents

    if validator not in contents:
        contents += "\n\ndef rule_" + str(rule.pk) + "(value):\n" + validator

    f = open(file_adress, "w+")
    f.write("".join(contents))
    f.close()


def addValidator(property, rule, validator):

    # Add the validator between the 
    modelspyText = addValidatorReference(property, rule)

    # Ensure that the import statement is correct
    importStatement = ( "from shared.validators import *")
    if importStatement not in modelspyText:
        modelspyText = importStatement + "\n" + modelspyText

    # Write the validator to validators.py
    addValidatorFunction(rule, validator)

    # Save text to models.py
    f = open("shared/models.py", "w")
    f.write("".join(modelspyText))
    f.close() 

def getStandardIfStatement(conditionalExpression, rule):
    return ("\tif " + conditionalExpression + ":\n"
        "\t\treturn True\n" 
        "\telse:\n" 
        "\t\traise ValidationError(\n"
        "\t\t\t'{value} does not abide by rule: '.format(value) + \'" +  rule.processed_text + "',\n"
        "\t\t\tparams={'value': value}, )\n"
        "\n\n")