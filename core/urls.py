from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .schema import swagger_urlpatterns

# from rest_framework.decorators import api_view
# from rest_framework.response import Response


# class LoginForm(AuthenticationForm):
#     captcha = fields.ReCaptchaField()
#
#     def clean(self):
#         captcha = self.cleaned_data.get("captcha")
#         if not captcha:
#             return
#         return super().clean()
#
#
# admin.site.login_form = LoginForm
# admin.site.login_template = "login.html"

#
# @api_view(["POST"])
# def test_email(request):
#     subject = "Test Email from Celery"
#     message = "This is a test email sent via Celery."
#     from_email = "primel040304@gmail.com"
#     recipient_list = ["jumayevjavohir585@gmail.com", "noktamov4@gmail.com"]
#     send_email_task.delay(subject, message, from_email, recipient_list)
#     return Response({"status": "email task queued"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/common/", include("apps.common.urls", namespace="common")),
    path("api/v1/", include("apps.user.urls", namespace="user")),
    path("api/v1/", include("apps.courses.urls", namespace="courses")),
    path("api/v1/", include("apps.news.urls", namespace="news")),
    # path("api/v1/test-email/", test_email, name="test_email"),
    path(
        "api/v1/payments/paylov/",
        include("apps.payment.paylov.urls", namespace="paylov"),
    ),
    path("api/v1/", include("apps.payment.urls", namespace="payment")),
]

urlpatterns += swagger_urlpatterns


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
