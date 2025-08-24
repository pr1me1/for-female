import time

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.common.models import BaseModel
from apps.courses.enums import WebinarStatus, FeeType


class Category(BaseModel):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    icon = models.ImageField(upload_to="category/icon", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


class Course(BaseModel):
    title = models.CharField(max_length=128, verbose_name="Title", db_index=True)
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Price")
    card = models.ImageField(
        upload_to="courses/%Y/%m", verbose_name="Card", blank=True, null=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name="Category",
        related_name="courses",
    )
    author = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        verbose_name="Author",
        related_name="courses",
    )
    discount = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name="Discount",
        default=0,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ("-created_at",)


class RatingCourse(BaseModel):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="rating_courses",
    )
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="rating_courses",
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    def __str__(self):
        return f"{self.user.username} - {self.course}"

    class Meta:
        verbose_name = "Rating Course"
        verbose_name_plural = "Rating Courses"
        ordering = ["-created_at"]


class Webinar(BaseModel):
    title = models.CharField(max_length=128, verbose_name="Title", db_index=True)
    author_display_name = models.CharField(
        max_length=128, verbose_name="Display Name", default="", db_index=True
    )
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Price")
    cover = models.ImageField(
        upload_to="webinars/%Y/%m", verbose_name="Card", blank=True, null=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Category",
        related_name="webinars",
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        verbose_name="Author",
        related_name="webinars",
    )
    datetime = models.IntegerField(
        default=int(time.time()),
    )
    status = models.CharField(
        choices=WebinarStatus.choices,
        default=WebinarStatus.UPCOMING,
        max_length=32,
        verbose_name="Status",
    )
    fee_type = models.CharField(
        choices=FeeType.choices,
        default=FeeType.FREE,
        max_length=32,
        verbose_name="Fee Type",
    )
    fee_amount = models.IntegerField(
        validators=[
            MinValueValidator(500),
            MaxValueValidator(99_999_999),
        ],
        null=True,
        blank=True,
        verbose_name="Fee Amount",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Webinar Course"
        verbose_name_plural = "Webinar Courses"


class RatingWebinar(BaseModel):
    webinar = models.ForeignKey(
        "courses.Webinar",
        on_delete=models.CASCADE,
        related_name="rating_webinar",
        verbose_name="Webinar",
    )
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="rating_webinar",
        verbose_name="User",
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name="Rating",
    )

    def __str__(self):
        return f"{self.user.username} - {self.webinar}"

    class Meta:
        verbose_name = "Rating Course"
        verbose_name_plural = "Rating Courses"
        ordering = ["-created_at"]


class Module(BaseModel):
    title = models.CharField(max_length=128, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        verbose_name="Module",
        related_name="modules",
    )
    icon = models.ImageField(upload_to="modules/%Y/%m", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"


class Lesson(BaseModel):
    title = models.CharField(max_length=128, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    file = models.FileField(upload_to="lessons/%Y/%m", null=True, blank=True)
    module = models.ForeignKey(
        "Module",
        on_delete=models.CASCADE,
        verbose_name="Module",
        related_name="lessons",
    )
    duration = models.IntegerField(
        verbose_name="Duration",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"


class Comment(BaseModel):
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        verbose_name="Comment",
        related_name="comments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Comment",
        related_name="comments",
        blank=True,
        null=True,
    )
    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        verbose_name="Comment",
        related_name="comments",
        blank=True,
        null=True,
    )
    text = models.TextField(verbose_name="Comment")
    rating = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name="Rating",
    )

    def __str__(self):
        return f"{self.user} {self.text[:10]}..."

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-rating"]
