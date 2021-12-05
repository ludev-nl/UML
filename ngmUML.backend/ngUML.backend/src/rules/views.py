''' Views manages api calls and returning JSON
    Knows little of how rules work, are stored etc.
    Decodes requests, calls RulesManager, correctly handles exceptions and JSON returns'''
from os import name
from django.http import JsonResponse # To return JSON
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponse
from textblob import TextBlob
import traceback

from rules.RulesManager.RulesManager import RulesManager
from rules.RulesManager.Terms import Operator, Value
from model.models import Classifier, Property
import json

rulesmanager = RulesManager()


def index(request):
    ''' Accepts GET requests to return all currently saved rules from the database as text. '''

    # Get rules from database
    rules_query = rulesmanager.get_all_rules()

    output = []

    for rule in rules_query:
        classifiers = []
        for classifier in rule[2].termlist.get_all(Classifier):
            classifiers.append({
                "name": classifier.name,
                "pk": classifier.pk
            })

        properties = []
        for property in rule[2].termlist.get_all(Property):
            properties.append({
                "pk": property.pk,
                "name": property.name,
                "classifier": property.classifier.name,
            })

        output.append({
            "pk": rule[1],
            "fields": {
                "original_input": rule[0],
                "processed_text": rule[2].get_processed_text(),
                "operator": rule[2].termlist.get_all(Operator),
                "value": rule[2].termlist.get_all(Value),
                "classifiers": classifiers,
                "properties": properties
            }
        })

    output = json.dumps(output)

    return HttpResponse(output, content_type='application/json')


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
        rulesmanager.add_rule(textrule)
    except Exception as err:
        # Return the error as JSON if exception
        print(traceback.format_exc())
        return JsonResponse({'FAIL' : 'Rule not saved to database',
        'type' : str(type(err)),
        'message' : str(err)},
        )
    return JsonResponse({'SUCCES' : 'Rule: ' + str(TextBlob(textrule).correct()) + " saved to rules."})

#CSRF exempt Turns off the need to provide a csrf token on a POST request. Temporary fix
@csrf_exempt
def remove(request):
    ''' Accepts POST requests to remove rules to the database. '''

    # Only accept POST requests
    if request.method != 'POST':
        return JsonResponse({'ERROR' : 'Only accepts POST requests, not: ' + request.method + " requests."})

    # Extract the rule pk from the request
    pk = request.POST.get('pk', -1) #give default value in case there is no rule argument
    if (pk == -1):
        return JsonResponse({'FAIL' : 'Supply pk : pk of rule to be removed in post argument'})

    # Remove the rule instance from database
    try:
        rulesmanager.remove_rule_by_pk(pk)
    except Exception as err:
        # Return the error as JSON if exception
        return JsonResponse({'FAIL' : 'Rule not removed from database',
        'type' : str(type(err)),
        'message' : str(err)},
        )
    return JsonResponse({'SUCCES' : 'Rule with pk: ' + pk + " removed from rules."})


#CSRF exempt Turns off the need to provide a csrf token on a POST request. Temporary fix
@csrf_exempt
def description(request):
    ''' Accepts GET requests to get the description of every rule. '''

    # Only accept POST requests
    if request.method != 'GET':
        return JsonResponse({'ERROR' : 'Only accepts GET requests, not: ' + request.method + " requests."})

    # Create a rule database object from the string
    try:
        description = RulesManager.get_description()
    except Exception as err:
        # Return the error as JSON if exception
        print(traceback.format_exc())
        return JsonResponse({'FAIL' : 'Could not retrieve the description information of the rules',
        'type' : str(type(err)),
        'message' : str(err)},
        )
    return JsonResponse({'SUCCES' : description})


def debug(request):
    ''' Function to test code in.
    Serves no practical purpose.'''
    from shared.models import Product

    prod = Product(price="21",name="John", location="store", description="type of grain")
    prod.full_clean()
    prod.save()


    return JsonResponse({'SUCCES' : 'it worked!'})
