from ..processors.TextProcessor import split_rule

class Rule:
    def __init__(self, textrule):
        ''' Constructor function'''
        # Rule for now is a string with a strict structure: 
        # "<classifier> <attribute> <condition> <value>"

        # Example:
        # "Warehouse storagecapacity atleast 50"

        rule = split_rule(textrule) # Process text (for now just a split function on ' ') (Just to showcase that the text processor can be used and expanded)
        self.classifier = rule[0] 
        self.attribute = rule[1]
        self.condition = rule[2]
        self.value = rule[3]

    def get_as_dict(self):
        ''' Returns the rule as a dictionary (JSON) with all individual properties as keys.'''

        return {
            'classifier': self.classifier,
            'attribute': self.attribute,
            'condition': self.condition,
            'value': self.value
        }

    def get_as_text(self):
        ''' Returns the entire rule as text '''
        return self.classifier + " " +  self.attribute + " " +  self.condition + " " + self.value


        

