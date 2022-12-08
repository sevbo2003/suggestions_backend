from rest_framework import viewsets, views
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import permissions
from rest_framework.decorators import action, api_view
from core.validators import validate_number
from core.code_generator import time_otp
import datetime


User = get_user_model()

# send sms
@api_view(['POST'])
def send_sms_code(request, format=None):
    user_phone_number = request.data.get('phone_number')
    if User.objects.get(username=user_phone_number):
        print("Your verification code is "+time_otp()+" and sent to "+user_phone_number)
        return Response({"time": datetime.datetime.now()}, status=status.HTTP_200_OK)
    return Response(status=400)
