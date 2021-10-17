#Decomposes text into representation of a rule, if possible

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