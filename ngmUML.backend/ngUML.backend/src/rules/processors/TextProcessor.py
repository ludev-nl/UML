#import rules to check if processed text is a rule
from nltk.corpus.reader.conll import ConllSRLInstance
from rules.RulesManager.Enums import Constraints
from rules.RulesManager.Rule import stringRule, numericalRule
'''The goal of text processor is to map messy_text into processed_text
That is to say: the user inputs messy text, and the text processor should unambigiously 
map all those possible inputs to the real, singular meaning
Example of user input: "I want the User class's name not to be longer than 20 characters"
Another example: "user's name should be less or equal to 20 letters"
Both map to: user name.length <= 20
'''


def split_rule(text):
    ''' Splits a string into individual words, just to showcase that the textprocessor is 
    now integrated and accessible for the rest of the project'''

     # Example:
        # "Warehouse storagecapacity atleast 50"
    #uncapatilize all words. 
    classifier = ["warehouse"]
    attribute = ["storagecapacity"]
    condition = ["atleast", "atmost"] 
    
    verify_components = text.lower().split()

    if( verify_components[0] not in classifier):
        print("error no classifier")
        return False
    
    if(verify_components[1] not in attribute):
        print("error no attribute")
        return False

    if(verify_components[2] not in condition):
        print("error no condition")
        return False

    if(not verify_components[3].isdecimal()):
        print("Error no numeric value")
        return False
    
    return True

#Each rule itself knows when the processed_text can be converted into that rule
def determine_rule_type(text):
    '''Checks if the processed string is of the form of one of the rules'''
    if(numericalRule.check_rule(text)):
        return Constraints.ATTR_OP_NUM
    elif(stringRule.check_rule(text)):
        return Constraints.ATTR_EQ_STR
    else:
        raise Exception("Can't parse into constraint: '" + text + "'")

#TODO:
#messy_text -> processed_text
#if the user gives input that maps to 1 single representation, convert it to that single representation
#example of user input: I want the User class's name not to be longer than 20 characters
#another example: user's name should be less or equal to 20 letters
#both map to: user name.length <= 20
def process_text(text):
    '''Maps messy user input to a singular representation'''
    return text




