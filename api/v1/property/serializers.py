from rest_framework import serializers

from property.models import Unit, Property
from accounts.models import TenantProfile
from api.v1.accounts.serializers import TenantProfileViewSerializer


class CreatePropertySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    address = serializers.CharField(max_length=128)
    location = serializers.CharField(max_length=128)
    features = serializers.CharField(max_length=128)


class ListUnitSerializer(serializers.ModelSerializer):
    assigned_tenant = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = (
            'id',
            'rent',
            'unit_type',
            'assigned_tenant'
        )

    def get_assigned_tenant(self, instance):
        request = self.context["request"]
        if (tenant_profiles := TenantProfile.objects.filter(units=instance, is_deleted=False)).exists():

            serialized__data = TenantProfileViewSerializer(
                tenant_profiles,
                context = {
                    "request" : request
                },
                many = True
            ).data

            return serialized__data
        else:
            return []


class ListPropertySerializer(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            'id',
            'name',
            'address',
            'location',
            'features',
            'unit',
        )

    def get_unit(self, instance):
        request = self.context["request"]
        units = instance.unit.filter(is_deleted=False)

        serialized_data = ListUnitSerializer(
            units,
            context = {
                "request" : request
            },
            many = True
        ).data
        

        return serialized_data

       