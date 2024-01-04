import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.db import transaction

from general.functions import generate_serializer_errors, loginUser
from general.encryptions import decrypt
from accounts.models import *
from property.models import Property, Unit
from api.v1.accounts.serializers import *
from general.decorators import group_required



@api_view(['POST'])
@permission_classes([AllowAny,])
def chief_profile_login(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = ChiefProfileLoginSerializer(data=request.data)
        if serialized_data.is_valid():
            email = request.data['email']
            password = request.data['password']
            if (chief_profile := ChiefProfile.objects.filter(email=email)).exists():
                chief_profile = chief_profile.latest('date_added')

                decrypted_password = decrypt(chief_profile.password)
                if decrypted_password == password:
                    access = loginUser(request, chief_profile.user)

                    transaction.commit()

                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "access" : access
                        }
                    }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Incorrect"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Chief profile does not exists"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }
        return Response({'app_data': response_data}, status=status.HTTP_200_OK)

    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

        return Response({'dev_data': response_data}, status=status.HTTP_200_OK)



@api_view(['POST'])
@group_required(['RealEstateAdmin'])
def create_tenant_profile(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = CreateTenantProfileSerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            phone = request.data["phone"]
            address = request.data["address"]
            adhar_card = request.data["adhar_card"]
            pan_card = request.data["pan_card"]
            agreement_end_date = request.data["agreement_end_date"]
            monthly_rent_date = request.data["monthly_rent_date"]
            monthly_rent_date = int(monthly_rent_date)

            if not TenantProfile.objects.filter(name=name, phone=phone,address=address).exists():

                tenant_profile = TenantProfile.objects.create(
                    name = name,
                    phone = phone,
                    address = address,
                    adhar_card = adhar_card,
                    pan_card = pan_card,
                    agreement_end_date = agreement_end_date,
                    monthly_rent_date = monthly_rent_date,
                    property = property
                )

                transaction.commit()

                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : "Tenant profile created successfully"
                    }
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Tenant profile already exists"
                    }
                }
            

        else:
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@group_required(['RealEstateAdmin'])
def list_tenant_profile(request):
    try:
        if (tenant_profiles := TenantProfile.objects.filter(is_deleted=False)).exists():

            serialized_data = TenantProfileViewSerializer(
                tenant_profiles,
                context = {
                    "request" : request
                },
                many = True
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : []
            }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(['RealEstateAdmin'])
def assign_unit_to_tenant(request, pk):
    try:
        transaction.set_autocommit(False)
        serialized_data = AssignUnitTenantSerializer(data=request.data)
        if serialized_data.is_valid():
            unit = request.data["unit"]
            property = request.data["property"]

            if (tenant_profile := TenantProfile.objects.filter(pk=pk, is_deleted=False)).exists():
                tenant_profile = tenant_profile.latest("date_added")

                if (unit := Unit.objects.filter(id=unit, is_deleted=False)).exists():
                    unit = unit.latest("date_added")

                    if (property_instance := Property.objects.filter(id=property)).exists():
                        property_instance = property_instance.latest("date_added")

                        if (unit_exists := property_instance.unit.filter(id=unit.id)).exists():
                            tenant_profile.units = unit
                            tenant_profile.save()
                            
                            transaction.commit()
                            response_data = {
                                "StatusCode" : 6000,
                                "data" : {
                                    "title" : "Success",
                                    "message" : "Unit assigned to a tenant under a property"
                                }
                            }
                        else:
                            response_data = {
                                "StatusCode" : 6001,
                                "data" : {
                                    "title" : "Failed",
                                    "message" : "Selected unit not found in selected property"
                                }
                            }
                    else:
                        response_data = {
                            "SatusCode" : 6000,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Property not found"
                            }
                        }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Unit not found"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Tanant profile not found"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)



