from enum import Enum

class Constraints(Enum):
    # <classifier> <attribute> <operator> <numerical value>
    # ex: wharehouse storagecapacity < 500
    ATTR_OP_NUM = "ATTR_OP_NUM"
    # <classifier> <attribute> <operator> <numerical value>
    # ex:employee name < 10
    MAX_SYMBOL = "MAX_SYMBOL"
    # <classifier> <attribute> <type>
    # ex: emloyee name letters
    SPECIFIC_CHAR = "SPECIFIC_CHAR"
    # <classifier> <attribute> <numerical value> <type> <numerical value> <type>
    # ex: employee zipcode 4 numbers 2 letters
    ORDER_CHAR = "ORDER_CHAR"
    # <classifier> <attribute>
    # ex: employee name
    NULL = "NULL"
    # <classifier> <attribute> <classifier> <attribute> <numerical value>
    # ex: employee vacationHours employee sickHours 240
    ATTRIBUTES_EQ_NUM = "ATTRIBUTES_EQ_NUM"
    NUM_SYMBOL = "NUM_SYMBOLS"
    TWO_TYPES = "TWO_TYPES"
    ONE_TYPE = "ONE_TYPE"
    
    UNKNOWN_TYPE = "UNKNOWN_TYPE"
