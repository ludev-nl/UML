#import rules to check if processed text is a rule
from nltk.corpus.reader.conll import ConllSRLInstance
import nltk
import re
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from model.models import Classifier, Property
from rules.processors.MappingProcessor import *

'''The goal of text processor is to map messy_text into processed_text
That is to say: the user inputs messy text, and the text processor should unambigiously
map all those possible inputs to the real, singular meaning
Example of user input: "I want the User class's name not to be longer than 20 characters"
Another example: "user's name should be less or equal to 20 letters"
Both map to: user name.length <= 20
'''
def wordToNumber(text):
    #if word does not need to be converged to number: put _NUMBER_
    units = {"zero": 0, "one" : 1, "two" : 2, "three" : 3, "four" : 4,  "five": 5, "six" : 6,
         "seven" : 7, "eight" : 8, "nine" : 9, "ten" : 10, "eleven" : 11, "twelve" : 12,
         "thirteen" : 13, "fourteen" : 14, "fifteen" : 15, "sixteen" :  16, "seventeen" : 17,
         "eighteen" : 18, "nineteen" : 19}
    tens = {"twenty": 20, "thirty" : 30, "fourty" : 40, "fifty" : 50, "sixty" : 60,
        "seventy": 70, "eighty" : 80, "ninety" : 90}
    amount = {"hundred" : 100, "thousand" : 1000, "million" : 1000000}

    newNumber, numbers, idNumbers = [], [], []
    copyText = text.copy()
    for i in range(len(copyText)):
      if(copyText[i] in units):
          numbers.append(units[copyText[i]])
          idNumbers.append(i)
      elif(copyText[i] in tens):
          numbers.append(tens[copyText[i]])
          idNumbers.append(i)
      elif(copyText[i] in amount):
          numbers.append(amount[copyText[i]])
          id = numbers.index(amount[copyText[i]])
          if(len(numbers) > 1):
            correctNumber = numbers[id-1] * numbers[id]
            numbers[id-1] = correctNumber
            del numbers[id]
            idNumbers.append(i)
      else:
          continue
    idNumbers.sort()
    newNumber.append(str(sum(numbers)))
    newText = copyText[0:idNumbers[0]] + newNumber + copyText[idNumbers[-1]+1:]
    return newText

def split_rule(text):
    ''' Splits a string into individual words and cleans the data'''
    text = text.lower() #set all symbols to lower case
    text = re.sub(r'[^\w\s]','',text) #remove puntuation
    textBlb = TextBlob(text).correct() #spell correction
    tokens = textBlb.tokens #split rule into seperate words
    text = [word for word in tokens if word not in stopwords.words('english')]#remove stopwords
    text = wordToNumber(text)
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(text[i]) for i in range(len(text))]
    return text

'''
#Each rule itself knows when the processed_text can be converted into that rule
def determine_rule_type(text):
    #Checks if the processed string is of the form of one of the rules
    if(numericalRule.check_rule(text)):
        return Constraints.PROP_OP_NUM
    elif(maxSymbolRule.check_rule(text)):
        return Constraints.MAX_SYMBOL
    elif(specificCharacterTypeRule.check_rule(text)):
        return Constraints.SPECIFIC_CHAR
    elif(characterOrderRule.check_rule(text)):
        return Constraints.ORDER_CHAR
    elif(nullRule.check_rule(text)):
        return Constraints.NULL
    elif(propertiesEqualValueRule.check_rule(text)):
        return Constraints.PROPERTIES_EQ_NUM
    else:
        raise Exception("Can't parse into constraint: '" + text + "'")
'''

#if the user gives input that maps to 1 single representation, convert it to that single representation
#example of user input: I want the User class's name not to be longer than 20 characters
#another example: user's name should be less or equal to 20 letters
#both map to: user name.length <= 20
#input: result of split_rule
def process_text(original_text):
    '''Maps messy user input to a singular representation'''
    all_classifiers = getClassifiers()
    all_properties = list()
    operators = list()
    #processed_text = "unknown"

    #Remove all classifiers that are not in the text
    #all_classifiers = list(set(original_text).intersection(set(classifier))) 
    temp = list()
    for classifier in all_classifiers:
        if classifier.name in original_text:
            temp.append(classifier)
    all_classifiers = temp

    # Get all properties from the classifiers in the text
    for classifier in all_classifiers:
        all_properties += getPropertiesFromClassifier(classifier)

    # Get only the properties that are in the text
    # properties = list(set(property_names) & set(original_text))
    temp = list()
    for property in all_properties:
        if property.name in original_text:
            temp.append(property)
    all_properties = temp

    # Get numeric words
    digits = [word for word in original_text.split(' ') if word.isnumeric()]

    # Get type key
    types = []
    for word in original_text.split(' '):
        if (word == "number" or word == "numbers" or word == "numeric" or word == "numerics"):
            types.append("NUMBERS")
        if (word == "letters"):
            types.append("LETTERS")

    """
    #regular expressions
    searchNull = re.compile(r"empty|null")
    searchNumSymbols = re.compile(r"symbols|characters")
    searchNot = re.compile(r"not|no")
    searchType = re.compile(r"LETTERS|NUMBERS")

    searchOp = re.compile(r"==|=|equal|copy|equivalent|double|like|match|<|less|lower|beneath|smaller|>|more|greater|higher|>=|least|fewest|minimum|<=|most|max|maximum")
    searchEqualOp = re.compile(r"==|=|equal|copy|equivalent|double|like|match")
    searchLessOp = re.compile(r"<|less|lower|beneath|smaller")
    searchMoreOp = re.compile(r">|more|greater|higher")
    searchLeastOp = re.compile(r">=|least|fewest|minimum")
    searchMostOp = re.compile(r"<=|most|max|maximum")

    #generate rule
    for token in original_text:
        if re.search(searchNull,token):#not null rule
            processed_text = classifier[0] + "." + all_properties[0].name + " NOT NULL"
            break
        if re.search(searchOp, token):#this is a rule with an operator
            if re.search(searchEqualOp, token):
                if re.search(searchNot, token):
                    operator = " != "
                    operators.append("!=")
                elif re.search(searchLessOp, token):
                    operator = " <= "
                    operators.append("<=")
                elif re.search(searchMoreOp,token):
                    operator = " >= "
                    operators.append(">=")
                else:
                    operator = " == "
                    operators.append("==")
            elif re.search(searchLessOp, token):
                operator = " < "
                operators.append("<")
            elif re.search(searchMoreOp, token):
                operator = " > "
                operators.append(">")
            elif re.search(searchLeastOp, token):
                operator = " >= "
                operators.append(">=")
            elif re.search(searchMostOp, token):
                operator = " <= "
                operators.append("<=")
            if re.search(searchNumSymbols, token):
                processed_text = all_classifiers[0].name + "." + all_properties[0].name + " CONTAINS" + operator + digits[0] +  " SYMBOLS"
                break
            else:
                processed_text = all_classifiers[0].name + "." + all_properties[0].name + operator + digits[0]
                break
        if (len(types)>0):#this rule contains a type specification
            if (len(digits) > 1):
                processed_text = all_classifiers[0].name + "." + all_properties[0].name + " CONTAINS " + digits[0] + " " + types[0] + " "+ digits[1] + " " + types[1]
                break
            else:
                processed_text = all_classifiers[0].name + "." + all_properties[0].name + " CONTAINS ONLY" + types[0]
                break
        if (len(all_properties) > 1):
            processed_text = all_classifiers[0].name + "." + all_properties[0].name + " " + all_classifiers[1].name + "." + all_properties[1].name + " EQUALS " + digits[0]
            break
        else:
            raise Exception("Can't parse into constraint: '" + processed_text + "'")
    """

    # All combinations of base operators and equivalent aliases
    operator_keywords = {
        "NULL": ["empty", "null"], 
        "SYMBOLS": ["symbols", "characters"], # Syntax: Class prop contains operator value SYMBOLS
        "NOT": ["not", "no"],
        "SPECIFICTYPE": ["LETTERS", "NUMBERS"],
        "==": ["==", "=", "equal", "copy", "equivalent", "double", "like", "match"],
        "<": ["<", "less", "lower", "beneath", "smaller"],
        ">": [">", "more", "greater", "higher"],
        ">=": [">=", "least", "fewest", "minimum"],
        "<=": ["<=", "most", "max", "maximum"],
    }

    for word in original_text:
        for key in operator_keywords:
            if word in operator_keywords[key]:
                operators.append(key)

    if len(operators) == 0: # Throw error if no operators are found
        raise Exception("Can't parse into constraint: '" + original_text + "'")
        

    return {
        "original_input": original_text,
        "structured language": text,
        "properties": all_properties,
        "classifiers": all_classifiers,
        "value": digits, 
        "operator": operators
    }
