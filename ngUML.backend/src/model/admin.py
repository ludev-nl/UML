from django.contrib import admin
from .models import Generalization, Property, Operation, Class, Enumerator, Association
# Register your models here.
admin.site.register(Generalization)
admin.site.register(Property)
admin.site.register(Operation)
admin.site.register(Class)
admin.site.register(Enumerator)
admin.site.register(Association)
