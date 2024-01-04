from django.contrib import admin

from property.models import *

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'location')

admin.site.register(Property, PropertyAdmin)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit_type', 'rent', 'property')

admin.site.register(Unit, UnitAdmin)

