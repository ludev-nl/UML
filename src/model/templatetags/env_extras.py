import os
from django import template

register = template.Library()

@register.simple_tag
def needs_restart():
    if os.environ.get('NGUML_NEEDS_RESTART') == 'true':
        return True
    else:
        return False