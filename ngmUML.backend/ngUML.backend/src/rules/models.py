import uuid
from django.db import models
from model.models import Classifier, Property

class Rule(models.Model):
    #id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)

    #original input
    original_input = models.TextField()
    processed_text = models.TextField()

    #one of Constraints
    type = models.TextField()

    operator = models.TextField()
    value = models.TextField()

    #links
    classifiers = models.ManyToManyField(Classifier)
    properties = models.ManyToManyField(Property)
