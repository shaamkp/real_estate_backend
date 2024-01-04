from django.db import models

from ckeditor.fields import RichTextField
from general.models import BaseModel


PROPERTY_UNIT_TYPE_CHOICES = (
    ("1bhk", "1BHK"),
    ("2bhk", "2BHK"),
    ("3bhk", "3BHK"),
    ("4bhk", "4BHK"),
)

class Property(BaseModel):
    name = models.CharField(max_length=128)
    address = models.TextField()
    location = models.CharField()
    features = RichTextField(null=True, blank=True)
    unit = models.ManyToManyField("property.Unit", blank=True)

    class Meta:
        db_table = 'property_property'
        verbose_name = 'property'
        verbose_name_plural = 'properties'
        ordering = ('id',)
    
    def __str__(self):
        return self.name
    

class Unit(BaseModel):
    rent = models.IntegerField()
    unit_type = models.CharField(choices=PROPERTY_UNIT_TYPE_CHOICES, null=True, blank=True, max_length=128)

    class Meta:
        db_table = 'property_unit'
        verbose_name = 'unit'
        verbose_name_plural = 'units'
        ordering = ('id',)

    def __str__(self):
        return self.unit_type


