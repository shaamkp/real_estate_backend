from django.db import models

from general.models import BaseModel

class ChiefProfile(BaseModel):
    email = models.EmailField(max_length=128)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    password = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'accounts_chief_profile'
        verbose_name = 'chief profile'
        verbose_name_plural = 'chief profiles'
        ordering = ('id',)


class TenantProfile(BaseModel):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    adhar_card = models.FileField(upload_to="accounts/tenant_profile/documents", null=True, blank=True)
    pan_card = models.FileField(upload_to="accounts/tenant_profile/documents", null=True, blank=True)
    units = models.ForeignKey("property.Unit", on_delete=models.CASCADE, null=True, blank=True)
    agreement_end_date = models.DateField(null=True, blank=True)
    monthly_rent_date = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'accounts_tenant_profile'
        verbose_name = 'tenant profile'
        verbose_name_plural = 'tenant profiles'
        ordering = ('id',)

    def __str__(self):
        return self.name



