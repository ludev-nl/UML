#import rules to check if processed text is a rule
from nltk.corpus.reader.conll import ConllSRLInstance
from rules.RulesManager.Enums import Constraints
from rules.RulesManager.Rule import stringRule, numericalRule
import nltk
import re
from nltk.corpus import stopwords
from textblob import TextBlob
'''The goal of text processor is to map messy_text into processed_text
That is to say: the user inputs messy text, and the text processor should unambigiously
map all those possible inputs to the real, singular meaning
Example of user input: "I want the User class's name not to be longer than 20 characters"
Another example: "user's name should be less or equal to 20 letters"
Both map to: user name.length <= 20
'''


def split_rule(text):
    ''' Splits a string into individual words and cleans the data'''
    text = text.lower() #set all symbols to lower case
    text = re.sub(r'[^\w\s]','',text) #remove puntuation
    textBlb = TextBlob(text).correct() #spell correction
    tokens = textBlb.tokens #split rule into seperate words
    filtered_tokens = [word for word in tokens if word not in stopwords.words('english')]#remove stopwords
    return filtered_tokens

#Each rule itself knows when the processed_text can be converted into that rule
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
    elif(characterOrderRule.check_rule(text)):
        return Constraints.ORDER_CHAR
    elif(nullRule.check_rule(text)):
        return Constraints.NULL
    elif(attributesEqualValueRule.check_rule(text)):
        return Constraints.ATTRIBUTES_EQ_NUM
    else:
        raise Exception("Can't parse into constraint: '" + text + "'")

#if the user gives input that maps to 1 single representation, convert it to that single representation
#example of user input: I want the User class's name not to be longer than 20 characters
#another example: user's name should be less or equal to 20 letters
#both map to: user name.length <= 20
#input: result of split_rule
def process_text(text):
    '''Maps messy user input to a singular representation'''
    attribute_words = ['id', 'first name', 'last name', 'name', 'address', 'email', 'number','no', 'code', 'date', 'type',
                       'volume', 'birth', 'password', 'price', 'quantity', 'location', 'maximum temperature', 'resolution date', 'creation date',
                       'crime code', 'course name', 'time slot', 'quantities', 'delivery date', 'prices',
                       'delivery address', 'scanner', 'till', 'illness conditions', 'diagnostic result', 'suggestions',
                       'birth date', 'order number', 'total cost', 'entry date', 'delivery status', 'description',
                       'product number']
    attributes = set(attribute_words) & set(text)
    other_nouns = [word for word in TextBlob(text).noun_phrases if word not in attributes]
    regExpr = re.compile(r"empty|null")
    for token in text:
        if re.search(regExpr,token):
                rule = other_nouns[0] + "." + attributes[0] + " NOT NULL"
                return rule
    return text
