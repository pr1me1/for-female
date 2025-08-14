from django.urls import path

from apps.payment.paylov.view import PaylovAPIView

app_name = "paylov"

urlpatterns = [
    path("callback/", PaylovAPIView.as_view(), name="paylov-callback"),
]
