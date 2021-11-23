#import rules to check if processed text is a rule
from nltk.corpus.reader.conll import ConllSRLInstance
import nltk
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from model.models import Classifier, Property
from rules.processors.MappingProcessor import *

#Preprocessing
#TODO: n't to not: shouldn't -> should not
#TODO: remove 's: Customer's name -> Customer name

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
    if(len(copyText) > 0 and len(idNumbers) > 0):
        newText = copyText[0:idNumbers[0]] + newNumber + copyText[idNumbers[-1]+1:]
        return newText
    else:
        return text

def split_rule(text):
    ''' Splits a string into individual words and cleans the data'''
    text = text.lower() #set all symbols to lower case
    text = re.sub(r'[^\w\s]-[<, =, >]','',text) #remove puntuation (fixed)
    textBlb = TextBlob(text).correct() #spell correction
    tokens = textBlb.tokens #split rule into seperate words
    text = wordToNumber(tokens)
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(text[i]) for i in range(len(text))]
    return text

#if the user gives input that maps to 1 single representation, convert it to that single representation
#example of user input: I want the User class's name not to be longer than 20 characters
#another example: user's name should be less or equal to 20 letters
#both map to: user name.length <= 20
#input: result of split_rule
def process_text(original_text):
    text = split_rule(original_text)
    '''Maps messy user input to a singular representation'''
    all_classifiers = getClassifiers()
    all_properties = list()
    operators = list()
    #processed_text = "unknown"

    #Remove all classifiers that are not in the text
    #all_classifiers = list(set(text).intersection(set(classifier))) 
    temp = list()
    for classifier in all_classifiers:
        if classifier.name.lower() in text:
            temp.append(classifier)
    all_classifiers = temp

    # Get all properties from the classifiers in the text
    for classifier in all_classifiers:
        all_properties += getPropertiesFromClassifier(classifier)

    # Get only the properties that are in the text
    # properties = list(set(property_names) & set(text))
    temp = list()
    for property in all_properties:
        if property.name.lower() in text:
            temp.append(property)
    all_properties = temp

    # Get numeric words
    digits = [word for word in text if word.isnumeric()]

    # All combinations of base operators and equivalent aliases
    operator_keywords = {
        "NULL": ["empty", "null"], 
        "NOT": ["not", "no"],
        "SYMBOLS": ["symbol", "character"], # Syntax: Class prop contains operator value SYMBOLS
        "LETTERS": ["letter", "alphabetical"],
        "NUMBERS": ["digit", "number", "numeric", "numerical"],
        "==": ["==", "=", "equal", "copy", "equivalent", "double", "like", "match"],
        "<": ["<", "less", "lower", "beneath", "smaller"],
        ">": [">", "more", "greater", "higher"],
        ">=": [">=", "least", "fewest", "minimum"],
        "<=": ["<=", "most", "max", "maximum"],
    }

    for word in text:
        for key in operator_keywords:
            if word.lower() in operator_keywords[key]:
                operators.append(key)
    

    if len(operators) == 0: # Throw error if no operators are found
        raise Exception("Can't parse into constraint: '" + " ".join(text) + "'")
        
    return {
        "original_input": original_text,
        "structured_language": text,
        "properties": all_properties,
        "classifiers": all_classifiers,
        "value": digits, # TODO: ability to insert words as value
        "operators": operators
    }