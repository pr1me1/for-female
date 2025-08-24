from django.core.validators import RegexValidator

alpha_validator = RegexValidator(
    regex=r"^[A-Za-z\s]+$", message="Must contain only Latin letters (A-Z, a-z)."
)
