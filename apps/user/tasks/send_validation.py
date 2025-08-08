from django.urls import reverse

from core.settings.base import DEFAULT_FROM_EMAIL
from core.task import send_email_task


def send_validation_email(email: str, token: str, request):
    validation_url = request.build_absolute_uri(
        reverse("apps.user:validation-endpoint") + f"?token={token}"
    )
    send_email_task.delay(
        subject="Validation Email",
        message=f"Click the link to validate your email: {validation_url}",
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
