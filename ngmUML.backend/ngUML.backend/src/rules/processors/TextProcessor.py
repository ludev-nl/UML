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
    text = [word for word in tokens if word not in stopwords.words('english')]#remove stopwords
    return text

#Each rule itself knows when the processed_text can be converted into that rule
def determine_rule_type(text):
    '''Checks if the processed string is of the form of one of the rules'''
    if(numericalRule.check_rule(text)):
        return Constraints.ATTR_OP_NUM
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
                       'crime code', 'course name', 'time slot', 'quantities', 'delivery date', 'prices', 'prize',
                       'delivery address', 'scanner', 'till', 'illness conditions', 'diagnostic result', 'suggestions',
                       'birth date', 'order number', 'total cost', 'entry date', 'delivery status', 'description',
                       'product number']
    attributes_text = set(attribute_words) & set(text)
    attributes = list(attributes_text)
    nouns = []
    for word,pos in nltk.pos_tag((text)):
         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
            if (word not in attributes):
             nouns.append(word)
    digits = [word for word in text if word.isnumeric()]
    types = []
    for word in text:
        if (word == "number" or word == "numbers" or word == "numeric" or word == "numerics"):
            types.append("NUMBERS")
        if (word == "letters"):
            types.append("LETTERS")

    #regular expressions
    searchNull = re.compile(r"empty|null")
    searchNumSymbols = re.compile(r"symbols|characters")
    searchNot = re.compile(r"not|no")
    searchType = re.compile(r"LETTERS|NUMBERS")

    searchOp = re.compile(r"==|=|equal|copy|equavilant|double|like|match|<|less|lower|beneath|smaller|>|more|greater|higher|>=|least|fewest|minimum|<=|most|max|maximum")
    searchEqualOp = re.compile(r"==|=|equal|copy|equavilant|double|like|match")
    searchLessOp = re.compile(r"<|less|lower|beneath|smaller")
    searchMoreOp = re.compile(r">|more|greater|higher")
    searchLeastOp = re.compile(r">=|least|fewest|minimum")
    searchMostOp = re.compile(r"<=|most|max|maximum")

    #generate rule
    for token in text:
        if re.search(searchNull,token):#not null rule
            text = nouns[0] + "." + attributes[0] + " NOT NULL"
            return text
        if re.search(searchOp, token):#this is a rule with an operator
            if re.search(searchEqualOp, token):
                if re.search(searchNot, token):
                    operator = " != "
                elif re.search(searchLessOp, token):
                    operator = " <= "
                elif re.search(searchMoreOp,token):
                    operator = " >= "
                else:
                    operator = " == "
            elif re.search(searchLessOp, token):
                operator = " < "
            elif re.search(searchMoreOp, token):
                operator = " > "
            elif re.search(searchLeastOp, token):
                operator = " >= "
            elif re.search(searchMostOp, token):
                operator = " <= "
            if (searchNumSymbols, token):
                text = nouns[0] + "." + attributes[0] + " CONTAINS" + operator + digits[0] +  " SYMBOLS"
                return text
            else:
                text = nouns[0] + "." + attributes[0] + operator + digit[0]
                return text
        if re.search(searchType, token):#this rule contains a type specification
            if (len(digits) > 1):
                text = nouns[0] + "." + attributes[0] + "CONTAINS" + digits[0] + " " + types[0] + " "+ digits[1] + " " + types[1]
                return text
            else:
                text = nouns[0] + "." + attributes[0] + " CONTAINS ONLY" + types[0]
                return text
        if (len(attributes)>1):
            text = nouns[0] + "." + attributes[0] + " " + nouns[1] + "." + attributes[1] + " EQUALS " + digits[0]
            return text
        else:
            raise Exception("Can't parse into constraint: '" + text + "'")
