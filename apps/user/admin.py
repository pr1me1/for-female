from django.contrib import admin

from apps.user.actions import soft_delete
from apps.user.models import User, UserProfile, Interest, UserInterest, UserCourse, UserWebinar


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active", "is_deleted",)
    readonly_fields = ("created_at", "updated_at")
    list_display_links = ("id", "email")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("id", "email", "username",)
    actions = [soft_delete]

    fieldsets = (
        (None, {"fields": ("username", "password", 'email')}),
        ("Permissions", {"fields": ("is_active", "is_deleted", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "<PASSWORD>", "<PASSWORD>"),
        })
    )

    filter_horizontal = ("groups", "user_permissions")


@admin.register(UserProfile)
class AccountProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    list_display_links = ("id", "user")

    fieldsets = (
        (None, {"fields": ("user", "first_name", "last_name")}),
        ("Additional fields", {"fields": ("phone_number", "bio", "avatar",)}),
    )


admin.site.register(Interest)
admin.site.register(UserInterest)
admin.site.register(UserCourse)
admin.site.register(UserWebinar)
