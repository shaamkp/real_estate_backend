import traceback
import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from django.db.models import Q

from django.db import transaction

from general.functions import generate_serializer_errors
from general.decorators import group_required
from property.models import *
from api.v1.property.serializers import *


@api_view(['POST'])
@group_required(['RealEstateAdmin'])
def create_property(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = CreatePropertySerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            address = request.data["address"]
            location = request.data["location"]
            features = request.data["features"]
            unit_ids = request.data.getlist("unit_ids")
            unit_ids = json.dumps(unit_ids)
            unit_ids = json.loads(unit_ids)

            if not Property.objects.filter(name=name, address=address, location=location).exists():

                property = Property.objects.create(
                    name = name,
                    address = address,
                    location = location,
                    features = features
                )

                if unit_ids:
                    for unit in unit_ids:
                        if (unit := Unit.objects.filter(id=unit)).exists():
                            unit = unit.latest("date_added")
                            property.unit.add(unit)
                        else:
                            pass
                
                property.save()
                transaction.commit()
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : "Property created successfully",
                    }
                }

        else:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "message": generate_serializer_errors(serialized_data._errors)
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
def list_units(request):
    try:
        if (units := Unit.objects.filter(is_deleted=False)).exists():

            serialized_data = ListUnitSerializer(
                units,
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


@api_view(['GET'])
@group_required(['RealEstateAdmin'])
def list_property(request):
    try:
        q = request.GET.get('q')
        if (property := Property.objects.filter(is_deleted=False)).exists():

            if q:
                property = property.filter(features__icontains=q)

            serialized_data = ListPropertySerializer(
                property,
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


@api_view(['GET'])
@group_required(['RealEstateAdmin'])
def property_profile_view(request, pk):
    try:
        if (property := Property.objects.filter(pk=pk, is_deleted=False)).exists():
            property = property.latest("date_added")

            serialized_data = ListPropertySerializer(
                property,
                context = {
                    "request" : request
                },
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



