from django.db import models

from apps.common.models import BaseModel
from apps.payment.enum import OrderStatus, ProviderChoices, TransactionStatus


class Order(BaseModel):
    user = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name='Customer',
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name='Course',
        null=True,
        blank=True,
    )
    webinar = models.ForeignKey(
        'courses.Webinar',
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name='Webinar',
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        'Amount',
        max_digits=10,
        decimal_places=2,
    )
    status = models.CharField(
        'Status',
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    is_paid = models.BooleanField()

    def __str__(self):
        return f'Order {self.id}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']


class Transaction(BaseModel):
    order = models.ForeignKey(
        'payment.Order',
        on_delete=models.SET_NULL,
        related_name="transactions",
        verbose_name='Order',
        null=True,
        blank=True,
    )
    provider = models.CharField(
        'Provider',
        max_length=100,
        verbose_name='Provider',
        choices=ProviderChoices.choices,
        default=ProviderChoices.PAYLOV,
    )
    status = models.CharField(
        'Status',
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
        max_length=100,
    )
    paid_at = models.DateTimeField(
        'Paid at',
        null=True,
        blank=True,
    )
    cancelled_at = models.DateTimeField(
        'Cancelled at',
        null=True,
        blank=True,
    )
    remote_id = models.CharField(
        'Remote ID',
        max_length=100,
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        'Amount',
        max_digits=10,
        decimal_places=2,
        verbose_name='Amount',
    )
    extra_data = models.JSONField()

    def __str__(self):
        return f'Transaction {self.id}'

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']

    @property
    def get_payment_url(self):
        payment_url = None
        if self.provider == ProviderChoices.PAYLOV:
            from apps.payments.paylov.client import PaylovClient

            payment_link = PaylovClient.create_payment_link(self)
