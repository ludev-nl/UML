from ..processors.TextProcessor import split_rule

class Rule:
    def __init__(self, text_rule):

        
        ''' Constructor function'''
        # Rule for now is a string with a strict structure: 
        # "<classifier> <attribute> <condition> <value>"

        # Example:
        # "Warehouse storagecapacity atleast 50"
        self.text_rule = text_rule
        #rule = split_rule(textrule) # Process text (for now just a split function on ' ') (Just to showcase that the text processor can be used and expanded)
        #self.classifier = rule[0] 
        #self.attribute = rule[1]
        
        #self.condition = rule[2]
        #self.value = rule[3]

    def check_rule(self):
        valid = False
        valid = split_rule(self.text_rule)
        return valid


    def get_as_dict(self):
        ''' Returns the rule as a dictionary (JSON) with all individual properties as keys.'''
        rule = self.text_rule.lower().split()
        return {
            'classifier': rule[0],
            'attribute': rule[1],
            'condition': rule[2],
            'value': rule[3]
        }

    def get_as_text(self):
        ''' Returns the entire rule as text '''
        return self.text_rule


        

