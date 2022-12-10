from django.urls import path

from apps.accounts.views import GenerateOTP, ValidateOTP, TestPermission

urlpatterns = [
    path('sms-send/', GenerateOTP.as_view(), name="generate"),
    path('sms-verify/', ValidateOTP.as_view(), name="validate"),
    path('test/', TestPermission.as_view(), name="test"),
]