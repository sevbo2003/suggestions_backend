from django.conf.urls import url

from .views import GenerateOTP, ValidateOTP, TestPermission

urlpatterns = [
    url(r'^generate/$', GenerateOTP.as_view(), name="generate"),
    url(r'^validate/$', ValidateOTP.as_view(), name="validate"),
    url(r'^test/$', TestPermission.as_view(), name="test"),
]