''' Views manages api calls and returning JSON 
    Knows little of how rules work, are stored etc.
    Decodes requests, calls RulesManager, correctly handles exceptions and JSON returns'''
from django.http import JsonResponse # To return JSON
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponse 
import traceback

from .RulesManager.RulesManager import RulesManager

rulesmanager = RulesManager()


def index(request):
    ''' Accepts GET requests to return all currently saved rules from the database as text. '''
    
    # Get rules from database
    rules_query = rulesmanager.db_get_all_rules()
    
    # Extract the properties needed and construct a rule list
    Rules_json = serializers.serialize("json", rules_query)

    return HttpResponse(Rules_json, content_type='application/json')


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
        print(traceback.format_exc())
        return JsonResponse({'FAIL' : 'Rule not saved to database',
        'type' : str(type(err)),
        'message' : str(err)},
        )
    return JsonResponse({'SUCCES' : 'Rule: ' + textrule + " saved to rules."})
    
#CSRF exempt Turns off the need to provide a csrf token on a POST request. Temporary fix
@csrf_exempt
def remove(request):
    ''' Accepts POST requests to add rules to the database. '''

    # Only accept POST requests
    if request.method != 'POST':
        return JsonResponse({'ERROR' : 'Only accepts POST requests, not: ' + request.method + " requests."})

    # Extract the rule pk from the request
    pk = request.POST.get('pk', -1) #give default value in case there is no rule argument
    if (pk == -1): 
        return JsonResponse({'FAIL' : 'Supply pk : pk of rule to be removed in post argument'})

    # Remove the rule instance from database
    try:
        rulesmanager.db_remove_rule_by_pk(pk)
    except Exception as err:
        # Return the error as JSON if exception
        return JsonResponse({'FAIL' : 'Rule not removed from database',
        'type' : str(type(err)),
        'message' : str(err)},
        )
    return JsonResponse({'SUCCES' : 'Rule with pk: ' + pk + " removed from rules."})


def debug(request):
    ''' Function to test code in.
    Serves no practical purpose.'''

    # Get rules from database
    rules = rulesmanager.get_all_rules()
    
    # Extract the properties needed and construct a rule list
    rule_list = []
    for rule in rules:
        rule_list.append(rule.get_as_dict()) # Get rule as a dictionary of properties

    return JsonResponse({'rules': rule_list})