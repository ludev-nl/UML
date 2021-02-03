import os
from django import template
from ..models import KVStorage

register = template.Library()

@register.simple_tag
def needs_restart():
    obj = KVStorage.objects.get_or_create(
        key='needs_restart',
        defaults={'value': 'false'}
    )
    if obj['value'] == 'true':
        return True
    else:
        return False 