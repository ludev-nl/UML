''' Views manages api calls and returning JSON 
    Knows little of how rules work, are stored etc.
    Decodes requests, calls RulesManager, correctly handles exceptions and JSON returns'''
from django.http import JsonResponse # To return JSON
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponse 

from .RulesManager.Rule import Rule as RuleClass # Rename to RuleClass as Rule is also an object/class in the database
from .RulesManager.RulesManager import RulesManager

rulesmanager = RulesManager()


def index(request):
    ''' Accepts GET requests to return all currently saved rules from the database as text. '''
    
    # Get rules from database
    rules_query = rulesmanager.db_get_all_rules()
    
    # Extract the properties needed and construct a rule list
    Rules_json = serializers.serialize("json", rules_query)

    return HttpResponse(Rules_json, content_type='application/json')


def get_modified_rules(request):
    ''' GET Request to showcase the integration of the API and the database with the tools folder and the RulesManager folder
    Serves no purpose at all except to showcase that it works.'''

    # Get rules from database
    rules = rulesmanager.get_all_rules()
    
    # Extract the properties needed and construct a rule list
    rule_list = []
    for rule in rules:
        rule_list.append(rule.get_as_dict()) # Get rule as a dictionary of properties

    return JsonResponse({'rules': rule_list})


#CSRF exempt Turns off the need to provide a csrf token on a POST request. Temporary fix
@csrf_exempt
def add(request):
    ''' Accepts POST requests to add rules to the database. '''

    # Only accept POST requests
    if request.method != 'POST':
        return JsonResponse({'ERROR' : 'Only accepts POST requests, not: ' + request.method + " requests."})

    # Extract the rule from the request
    textrule = request.POST.get('rule', "") #give default value in case there is no rule argument
    if (textrule == ""): 
        return JsonResponse({'FAIL' : 'Supply rule : ruletext in post argument'})

    # Create a rule database object from the string
    try:
        rulesmanager.db_add_rule(textrule)
    except Exception as err:
        # Return the error as JSON if exception
        return JsonResponse({'FAIL' : 'Rule not saved to database',
        'type' : str(type(err)),
        'message' : str(err)},
        )
    return JsonResponse({'SUCCES' : 'Rule: ' + textrule + " saved to rules."})
    
