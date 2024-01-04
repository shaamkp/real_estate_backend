from rest_framework import serializers

from accounts.models import TenantProfile
from property.models import Property, Unit


class ChiefProfileLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class CreateTenantProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    adhar_card = serializers.FileField()
    pan_card = serializers.FileField()
    agreement_end_date = serializers.CharField()
    monthly_rent_date = serializers.CharField()
    property = serializers.CharField()


class TenantProfileViewSerializer(serializers.ModelSerializer):
    pan_card = serializers.SerializerMethodField()
    adhar_card = serializers.SerializerMethodField()

    class Meta:
        model = TenantProfile
        fields = (
            'id',
            'name',
            'phone',
            'address',
            'adhar_card',
            'pan_card',
            'agreement_end_date',
            'monthly_rent_date',
            
        )

    def get_pan_card(self, instance):
        request = self.context["request"]
        if instance.pan_card:
            return request.build_absolute_uri(instance.pan_card.url)
        else:
            return None
        
    def get_adhar_card(self, instance):
        request = self.context["request"]
        if instance.adhar_card:
            return request.build_absolute_uri(instance.adhar_card.url)
        else:
            return None
    
        

class AssignUnitTenantSerializer(serializers.Serializer):
    unit = serializers.CharField()
    property = serializers.CharField()
