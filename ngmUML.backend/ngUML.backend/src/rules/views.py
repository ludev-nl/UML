from .models import *
from django.http import JsonResponse # To return JSON
from django.views.decorators.csrf import csrf_exempt

from .RulesManager.Rule import Rule as RuleClass # Rename to RuleClass as Rule is also an object/class in the database


def index(request):
    ''' Accepts GET requests to return all currently saved rules from the database as text. '''
    
    # Get rules from database
    rules_query = Rule.objects.all()
    
    # Extract the properties needed and construct a rule list
    rule_list = []
    for rule in rules_query:
        rule_list.append(str(rule.rule))

    return JsonResponse({'rules': rule_list})


def get_modified_rules(request):
    ''' GET Request to showcase the integration of the API and the database with the tools folder and the RulesManager folder
    Serves no purpose at all except to showcase that it works.'''

    # Get rules from database
    rules_query = Rule.objects.all()
    
    # Extract the properties needed and construct a rule list
    rule_list = []
    for rule in rules_query:
        rule = RuleClass(str(rule.rule)) # Convert Database rule object to a Rule object from the custom Rule class
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
    textrule = request.POST['rule']

    # Create a rule database object from the string
    rule = Rule(rule=textrule)
    
    # Save Rule to database
    rule.save()

    return JsonResponse({'SUCCES' : 'Rule: ' + textrule + " saved to rules."})
