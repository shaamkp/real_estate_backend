from mailqueue.models import MailerMessage

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password

from accounts.models import ChiefProfile
from general.encryptions import encrypt


def generate_serializer_errors(args):
    message = ""
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        # message += "%s : %s | " %(key,error_message)
        message += f"{key} - {error_message} | "
    return message[:-3]


def loginUser(request, user):
    try:
        login(request,user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        access = {
            "access": access_token,
            "refresh": str(refresh)
        }
        return access
    except:
        error = {
            "message": "User could not be verified"
        }

def CreateChiefUser(email,password):
    if not ChiefProfile.objects.filter(email=email):
        user = User.objects.create(
            username = email,
            password = make_password(password),
        )
        group_name = 'RealEstateAdmin'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        chief_profile = ChiefProfile.objects.create(
            email = email,
            password = encrypt(password),
            user = user
        )
        return "user created"
    else:
        return "user already exists"
    


            


