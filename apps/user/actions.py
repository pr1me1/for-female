from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.db.transaction import atomic

User = get_user_model()


@admin.action(description="perform soft delete")
def soft_delete(modeladmin, request, queryset):
    from django.utils import timezone

    timestamp = int(timezone.now().timestamp())
    users = list(queryset)

    for user in users:
        user.soft_delete()

    with atomic():
        User.objects.bulk_update(users, ["email", "is_deleted", "is_active"])

    messages.success(request, f"{len(users)} users were deleted successfully")
