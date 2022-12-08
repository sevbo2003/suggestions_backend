from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import send_sms_code

# router = DefaultRouter()
# router.register(r'register', UserRegisterViewSet, basename='register')

urlpatterns = [
    # path('', include(router.urls)),
    path('send_sms_code/', send_sms_code, name='send_sms_code'),
]