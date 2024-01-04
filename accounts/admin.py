from django.contrib import admin

from accounts.models import ChiefProfile, TenantProfile


class ChiefProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')

admin.site.register(ChiefProfile, ChiefProfileAdmin)


class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'units', 'agreement_end_date', 'monthly_rent_date', 'adhar_card', 'pan_card')

admin.site.register(TenantProfile, TenantProfileAdmin)
