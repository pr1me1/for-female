import datetime

from django.db import models, transaction

from apps.common.models import BaseModel
from apps.payment.enum import OrderStatus, ProviderChoices, TransactionStatus


class Providers(BaseModel):
    name = models.CharField(
        max_length=255, verbose_name="Name", choices=ProviderChoices.choices
    )
    key = models.CharField(max_length=255, verbose_name="Key")

    def __str__(self):
        return f"Provider: {self.name}"

    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"


class ProviderCredentials(BaseModel):
    provider = models.ForeignKey("payment.Providers", on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    key_description = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            "provider",
            "key",
        )
        verbose_name = "Provider Credential"
        verbose_name_plural = "Provider Credentials"

    def __str__(self):
        return f"{self.provider} - {self.key}"


class Order(BaseModel):
    user = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name="Customer",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name="Course",
        null=True,
        blank=True,
    )
    webinar = models.ForeignKey(
        "courses.Webinar",
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name="Webinar",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        "Amount",
        max_digits=10,
        decimal_places=2,
    )
    status = models.CharField(
        "Status",
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]


class Transaction(BaseModel):
    order = models.ForeignKey(
        "payment.Order",
        on_delete=models.SET_NULL,
        related_name="transactions",
        verbose_name="Order",
        null=True,
        blank=True,
    )
    provider = models.CharField(
        "Provider",
        max_length=100,
        choices=ProviderChoices.choices,
        default=ProviderChoices.PAYLOV,
    )
    status = models.CharField(
        "Status",
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
        max_length=100,
    )
    paid_at = models.DateTimeField(
        "Paid at",
        null=True,
        blank=True,
    )
    cancelled_at = models.DateTimeField(
        "Cancelled at",
        null=True,
        blank=True,
    )
    remote_id = models.CharField(
        verbose_name="Remote ID",
        max_length=100,
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        "Amount",
        max_digits=10,
        decimal_places=2,
    )
    extra_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.id}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]

    @property
    def get_payment_url(self):
        payment_link = None
        if self.provider.name == ProviderChoices.PAYLOV:
            from apps.payment.paylov.client import PaylovClient

            payment_link = PaylovClient.create_payment_url(self)

        return payment_link

    def apply_transaction(
        self,
        provider=None,
        transaction_id: str | None = None,
    ):
        if not self.remote_id and transaction_id:
            self.remote_id = str(transaction_id)
        self.provider = provider
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(provider)
        print(self.provider)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.paid_at = datetime.datetime.now()
        self.status = TransactionStatus.COMPLETED

        try:
            with transaction.atomic():
                self.save(
                    update_fields=[
                        "paid_at",
                        "status",
                        "remote_id",
                    ]
                )
                self.order.status = OrderStatus.COMPLETED
                self.order.is_paid = True if self.paid_at else False
                self.order.save(update_fields=["is_paid", "status"])
        except Exception:
            raise

        return self

    def cancel_transaction(self, reason):
        self.cancelled_at = datetime.datetime.now()
        self.status = TransactionStatus.CANCELLED
        self.extra = {"payme_cancel_reason": reason}
        self.save(
            update_fields=[
                "cancelled_at",
                "status",
            ]
        )

        self.order.paid_at = None
        self.order.save(update_fields=["is_paid"])

        return self


class UserCard(BaseModel):
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="user_cards",
        verbose_name="User",
    )
    card_token = models.CharField(max_length=255, verbose_name="Card Token")
    provider = models.ForeignKey(
        "payment.Providers", on_delete=models.CASCADE, verbose_name="Provider"
    )
    cardholder_name = models.CharField(
        max_length=255, verbose_name="Cardholder Name", null=True, blank=True
    )
    last_four_digits = models.CharField(
        max_length=4, verbose_name="Last Four Digits", null=True, blank=True
    )
    brand = models.CharField(
        max_length=255, verbose_name="Brand", null=True, blank=True
    )
    expire_month = models.CharField(max_length=2, verbose_name="Expire Month")
    expire_year = models.CharField(max_length=4, verbose_name="Expire Year")
    is_confirmed = models.BooleanField(default=False, verbose_name="Is confirmed")

    class Meta:
        verbose_name = "User Card"
        verbose_name_plural = "User Cards"

    def __str__(self):
        return f"User Card: {self.id}"
