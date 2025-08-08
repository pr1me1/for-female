from django.db import models

from apps.common.models import BaseModel
from apps.courses.models import Course
from apps.news.enums import QuestionTypeChoices
from apps.user.models import User


class Post(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    card = models.ImageField(verbose_name="Card", upload_to="cards/", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Event(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    card = models.ImageField(verbose_name="Card", upload_to="cards/", null=True, blank=True)
    date = models.DateField(verbose_name="Date")
    location = models.CharField(max_length=255, verbose_name="Location")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


class Survey(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    card = models.ImageField(verbose_name="Card", upload_to="cards/", null=True, blank=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Course",
        related_name="surveys",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"


class Question(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    type = models.CharField(
        choices=QuestionTypeChoices.choices,
        max_length=128,
        verbose_name="Type"
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        verbose_name="Survey",
        related_name="questions",
    )
    file = models.FileField(verbose_name="File", upload_to="files/", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class QuestionOption(BaseModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Question",
        related_name="options",
    )
    title = models.CharField(max_length=255, verbose_name="Title")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "QuestionOption"
        verbose_name_plural = "QuestionOptions"


class Submission(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="submissions",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Question",
        related_name="submissions",
    )
    chosen_option = models.ForeignKey(
        QuestionOption,
        on_delete=models.CASCADE,
        verbose_name="Chosen Option",
        related_name="submissions",
        null=True,
        blank=True,
    )
    text = models.TextField(verbose_name="Text", null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.question}"

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
