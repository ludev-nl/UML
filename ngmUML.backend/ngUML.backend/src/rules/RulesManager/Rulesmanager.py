#Class that handles logic of api calls to rules
#Like: addRule(attributes...), removeRule(id), editRule(request), getAllRules(), getRule(id)

# Note: split the logic of views and the business logic of rulesmanager logically, don't just move logic from views.py to rulesmanger when there is no need for it