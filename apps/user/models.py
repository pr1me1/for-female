from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from apps.common.models import BaseModel
from apps.courses.models import Course, Webinar
from apps.user.enums import ReasonDeleteChoices
from apps.user.manager import UserManager
from apps.user.services.avatar_upload import avatar_upload_path


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False, db_index=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username if self.username else self.email

    def soft_delete(self):
        import time

        timestamp = int(time.time())
        self.email = f"{self.email}_deleted_{timestamp}"
        self.is_deleted = True
        self.is_active = False
        try:
            profile = self.profile
            profile.soft_delete()
        except UserProfile.DoesNotExist:
            pass
        self.save()

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['username'],
                name="unique_active_username",
                condition=models.Q(is_deleted=False),
            )
        ]

        indexes = [
            models.Index(
                fields=["is_active", "is_deleted"]
            )
        ]


class UserProfile(BaseModel):
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="User",
    )
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    phone_number = models.CharField(
        max_length=50,  # increased bcz of suffixes
        validators=[
            RegexValidator(
                regex=r'^\+998\d{9}$',
                message="Phone number must be entered in the format: '+998xxxxxxx'. Up to 15 digits allowed."
            )
        ],
        null=True,
        blank=True
    )
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)
    bio = models.TextField(max_length=256, null=True, blank=True)
    reason_delete = models.CharField(
        choices=ReasonDeleteChoices.choices,
        max_length=64,
        null=True,
        blank=True,
    )
    reason_delete_str = models.TextField(null=True, blank=True, max_length=256)
    interests = models.ManyToManyField(
        'Interest',
        through='UserInterest',
        blank=True,
        related_name="user_interests",
        null=True,
    )

    def soft_delete(self):
        import time
        timestamp = int(time.time())
        if self.phone_number:
            self.phone_number = f"{self.phone_number}_deleted_{timestamp}"
        self.save()

    def __str__(self):
        return f"Profile of {self.user.email}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        indexes = [
            models.Index(fields=["phone_number"])
        ]


class Interest(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Interest"
        verbose_name_plural = "Interests"
        indexes = [
            models.Index(fields=["name"])
        ]


class UserInterest(BaseModel):
    interest = models.ForeignKey(
        'Interest',
        on_delete=models.CASCADE,
        related_name="interest_user_relations",
        blank=True,
        null=True,
    )
    user_profile = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        related_name="user_interest_relations",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Interest of {self.user_profile.first_name} {self.user_profile.last_name}"

    class Meta:
        verbose_name = "User Interest"
        verbose_name_plural = "User Interests"
        constraints = [
            models.UniqueConstraint(
                fields=['user_profile', 'interest'],
                name='unique_user_interest'
            )
        ]


class UserCourse(BaseModel):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name="user_course_relations",
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name="user_course_relations",
    )

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "User Course"
        verbose_name_plural = "User Courses"


class UserWebinar(BaseModel):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name="user_webinar_relations",
    )
    webinar = models.ForeignKey(
        'courses.Webinar',
        on_delete=models.CASCADE,
        related_name="user_webinar_relations",
    )

    def __str__(self):
        return f"{self.user} - {self.webinar}"

    class Meta:
        verbose_name = "User Webinar"
        verbose_name_plural = "User Webinars"
