from enum import Enum

class Constraints(Enum):
    # <classifier> <attribute> <operator> <numerical value>
    # ex: wharehouse storagecapacity < 500
    ATTR_OP_NUM = "ATTR_OP_NUM"
    # <classifier> <attribute> <(not) equal> <string>
    # ex: employee name != 'John Cena'
    ATTR_EQ_STR = "ATTR_EQ_STR"
    #TODO: Enumerate other constraint types
