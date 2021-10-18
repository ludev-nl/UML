import uuid
from django.db import models

# Create your models here.
class Rule(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)

    #original input
    messy_rule = models.TextField()

    #unambigious rule
    processed_rule = models.TextField()
    
    #one of Constraints
    type = models.TextField()

    python = models.TextField()
