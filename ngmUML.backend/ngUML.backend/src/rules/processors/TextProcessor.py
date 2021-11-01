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
    #possible input:
        # ATTRIBUTE from OBJECT is not null
        # ATTRIBUTE from OBJECT should consist of NUMBER of symbols
        # ATTRIBUTE from OBJECT should only consist out of TYPE
        # ATTRIBUTE1 from OBJECT and ATTRIBUTE2 from OBJECT should add up to NUMBER
        # ATTRIBUTE from OBJECT should consist out of NUMBER of TYPE followed by NUMBER of TYPE
        # ATTRIBUTE from OBJECT ==/!= STRING
	    # ATTRIBUTE from OBJECT should be OPERATOR NUMBER
    #desired output:
        # NULL: <classifier> <attribute>
        # MAX_SYMBOL: <classifier> <attruibute> <operator> <numerical value>
        # SPECIFIC_CHAR: <classifier> <attribute> <type>
        # ATTRIBUTES_EQ_NUM: <classifier> <attribute> <classifier> <attribute> <numerical value>
        # ORDER_CHAR: <classifier> <attribute> <numerical value> <type> <numerical value> <type>
        # ATTR_EQ_STR: <classifier> <attribute> <==/!=> <string>
        # ATTR_OP_NUM: <classifier> <attribute> <operator> <numerical value>

    component = text.lower().split()
    if (len(components) > 15 ):
        raise Exception("Text is too long please formulate in 15 words or less")

    #check rule and return type
    if component[3] is 'is':
        text = component[2] + ' ' + component[0]
        if (nullRule.check_rule(text)):
            return Constraints.NULL
    if component[4] is 'consists':
        text = component[2] + ' ' + component[0] + ' ' + component[6] + ' ' + component[8]
        if (maxSymbolRule.check_rule(text)):
            return Constraints.MAX_SYMBOL
    if component[4] is 'only':
        text = component[2] + ' ' + component[0] + ' ' + component[8]
        if (specificCharacterTypeRule.check_rule(text)):
            return Constraints.SPECIFIC_CHAR
    if component[10] is 'followed':
        text = component[2] + ' ' + component[0] + ' ' + component[6] + ' ' + component[4] + ' ' + component [11]
        if (attributesEqualValueRule.check_rule(text)):
            return Constraints.ATTRIBUTES_EQ_NUM
    if component[8] is 'add':
        text = component[2] + ' ' + component[0] + ' ' + component[7] + ' ' + component[9] + ' ' + component[12] + ' ' + component[14]
        if (characterOrderRule.check_rule(text)):
            return Constraints.ORDER_CHAR
    if component[-1].isalpha():
        text = component[2] + ' ' + component[0] + ' ' + component[3] + component[4]
        if (stringRule.check_rule(text)):
            return Constraints.ATTR_EQ_STR
    if component[-1].isnumeric():
        text = component[2] + ' ' + component[0] + ' ' + component[5] + component[-1]
        if (numericalRule.check_rule(text)):
            return Constraints.ATTR_OP_NUM
    #return Constraints.UNKNOWN_TYPE
    raise Exception("Can't parse into constraint: '" + text + "'")

#Each rule itself knows when the processed_text can be converted into that rule
#TODO: merge with split_rule? add other types
def determine_rule_type(text):
    '''Checks if the processed string is of the form of one of the rules'''
    if(numericalRule.check_rule(text)):
        return Constraints.ATTR_OP_NUM
    elif(stringRule.check_rule(text)):
        return Constraints.ATTR_EQ_STR
    elif(maxSymbolRule.check_rule(text)):
        return Constraints.MAX_SYMBOL
    elif(specificCharacterTypeRule.check_rule(text)):
        return Constraints.SPECIFIC_CHAR
    else:
        raise Exception("Can't parse into constraint: '" + text + "'")

#TODO:
#messy_text -> processed_text ??in split_rule?
#if the user gives input that maps to 1 single representation, convert it to that single representation
#example of user input: I want the User class's name not to be longer than 20 characters
#another example: user's name should be less or equal to 20 letters
#both map to: user name.length <= 20

    #Idea:
    # catagories of words for NLP:
    # subtyping_word = ['is a', 'is a kind of', 'is', 'can be', 'are', 'can involve', 'be', 'should be']
    # operators = ["at most", "at least", "more than", "less than", "equal to or more than", "equal to or less than", "greater than"]
    # type_words = ["numbers", "letters"]
def process_text(text):
    '''Maps messy user input to a singular representation'''
    return text
