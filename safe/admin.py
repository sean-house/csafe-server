from django.contrib import admin
from safe.models import Safe, Relationship, User, UserAttributes, Safe_Event

# Register your models here.
admin.site.register(Safe)
admin.site.register(Relationship)
admin.site.register(UserAttributes)
admin.site.register(Safe_Event)