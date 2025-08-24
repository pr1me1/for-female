from django.urls.conf import path

from apps.payment.views import OrderCreateAPIView, DeleteOrderAPIView
from apps.payment.views.card import (
    AddCardAPIView,
    ConfirmUserCardAPIView,
    DeleteUserCardAPIView,
    ListUserCardsAPIView,
    GetSingleUserCardAPIView,
    UserCardReceiptCreateAPIView,
    UserCardReceiptConfirmAPIView,
)
from apps.payment.views.transaction import TransactionListAPIView

app_name = "payment"

urlpatterns = [
    path("order/create/", OrderCreateAPIView.as_view(), name="create-order"),
    path("order/<int:pk>/delete/", DeleteOrderAPIView.as_view(), name="delete-order"),
    path("transactions/", TransactionListAPIView.as_view(), name="transaction-list"),
    path("card/create/", AddCardAPIView.as_view(), name="card-create"),
    path("card/confirm/", ConfirmUserCardAPIView.as_view(), name="card-confirm"),
    path("card/delete/", DeleteUserCardAPIView.as_view(), name="card-delete"),
    path("card/<int:user_id>/list/", ListUserCardsAPIView.as_view(), name="card-list"),
    path("card/<str:card_id>/", GetSingleUserCardAPIView.as_view(), name="card-get"),
    path(
        "card/receipt/create/",
        UserCardReceiptCreateAPIView.as_view(),
        name="create-receipt",
    ),
    path(
        "card/receipt/pay/", UserCardReceiptConfirmAPIView.as_view(), name="pay-receipt"
    ),
]
