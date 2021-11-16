#import rules to check if processed text is a rule
from nltk.corpus.reader.conll import ConllSRLInstance
from rules.RulesManager.Enums import Constraints
from rules.RulesManager.Rule import numericalRule
import nltk
import re
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from model.models import Classifier, Property

'''The goal of text processor is to map messy_text into processed_text
That is to say: the user inputs messy text, and the text processor should unambigiously
map all those possible inputs to the real, singular meaning
Example of user input: "I want the User class's name not to be longer than 20 characters"
Another example: "user's name should be less or equal to 20 letters"
Both map to: user name.length <= 20
'''
def wordToNumber(text):
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

#Each rule itself knows when the processed_text can be converted into that rule
def determine_rule_type(text):
    '''Checks if the processed string is of the form of one of the rules'''
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

#if the user gives input that maps to 1 single representation, convert it to that single representation
#example of user input: I want the User class's name not to be longer than 20 characters
#another example: user's name should be less or equal to 20 letters
#both map to: user name.length <= 20
#input: result of split_rule
def process_text(text):
    '''Maps messy user input to a singular representation'''
    all_classifier = list()
    all_properties = list()
    for classifier in Classifier.classifier.all():
        all_classifier.append(classifier.name)
    classifier = list(set(text).intersection(set(classifier)))
    for object in classifier:
        for property in Property.classifier.filter(classifier=Classifier.classifier.filter(name=object)):
            all_properties.append(property.name)
    properties = list(set(all_properties) & set(text))
    digits = [word for word in text if word.isnumeric()]
    types = []
    for word in text:
        if (word == "number" or word == "numbers" or word == "numeric" or word == "numerics"):
            types.append("NUMBERS")
        if (word == "letters"):
            types.append("LETTERS")
# return {
#         "original_input": text,
#         "properties": [property],
#         "classifiers": [classifier],
#         "value": value,
#         "operator": "==", 
#     }
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
            text = classifier[0] + "." + properties[0] + " NOT NULL"
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
            if re.search(searchNumSymbols, token):
                text = classifier[0] + "." + properties[0] + " CONTAINS" + operator + digits[0] +  " SYMBOLS"
                return text
            else:
                text = classifier[0] + "." + properties[0] + operator + digits[0]
                return text
        if (len(types)>0):#this rule contains a type specification
            if (len(digits) > 1):
                text = classifier[0] + "." + properties[0] + " CONTAINS " + digits[0] + " " + types[0] + " "+ digits[1] + " " + types[1]
                return text
            else:
                text = classifier[0] + "." + properties[0] + " CONTAINS ONLY" + types[0]
                return text
        if (len(properties)>1):
            text = classifier[0] + "." + properties[0] + " " + classifier[1] + "." + properties[1] + " EQUALS " + digits[0]
            return text
        else:
            raise Exception("Can't parse into constraint: '" + text + "'")
