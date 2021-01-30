from django.shortcuts import HttpResponse, redirect
from shutil import copyfile
import os
import threading
import sys
from ..models import *
from django.conf import settings
from django.utils import autoreload

def clear(request):
    models = settings.BASE_DIR + '/shared/models.py'
    default = settings.BASE_DIR + '/shared/models.default.py'
    copyfile(
        default,
        models
    )
    notDelete = [
        '__init__.py',
        'views.py',
        'newclassifier.py',
        'otherclassifier.py'
    ]
    for f in os.listdir(settings.BASE_DIR + '/shared/views'):
        if f not in notDelete:
             os.remove(
                 settings.BASE_DIR + '/shared/views/' + f
             )
    for c in Class.objects.all():
        c.delete()
    for c in Classifier.objects.all():
        c.delete()
    for p in Property.objects.all():
        p.delete()
    for o in Operation.objects.all():
        o.delete()
    for g in Generalization.objects.all():
        g.delete()
    for op in OperationParameter.objects.all():
        op.delete()
    for a in Association.objects.all():
        a.delete()
    for c in Composition.objects.all():
        c.delete()
    for r in Relationship.objects.all():
        r.delete()
    #ar = autoreload.restart_with_reloader()
    # -> THIS RESTARTS THE SERVER BUT THE PORT WILL BE IN USE
    # -> POSSIBLE FIX?
    #sys.exit(ar)
    return redirect('/model')
    
def generate(request):
    # code to generate
    return redirect('/model')
