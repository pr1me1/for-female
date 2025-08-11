from django.db.models.enums import TextChoices


class WebinarStatus(TextChoices):
    LIVE = "live",
    COMPLETED = "completed",
    UPCOMING = "upcoming",

class FeeType(TextChoices):
    FREE = "free",
    PAID = "paid"
