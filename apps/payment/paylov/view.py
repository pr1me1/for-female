from collections.abc import Callable
from typing import Any, ClassVar

from django.db import transaction as db_transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.enum import TransactionStatus
from apps.payment.models import Providers, Transaction
from apps.payment.paylov.auth import authentication as paylov_authentication
from apps.payment.paylov.client import PaylovClient
from apps.payment.paylov.constants import PaylovMethods, STATUS_CODES, STATUS_TEXT
from apps.payment.paylov.serializer import PaylovSerializer


class PaylovAPIView(APIView):
    """
    API view for handling Paylov transactions.

    This view manages the processing of Paylov transactions
    using the specified methods for checking and performing transactions.
    It handles authentication, serialization, and execution of transaction
    methods atomically.
    """

    permission_classes = [AllowAny]
    http_method_names = ("post",)
    authentication_classes: ClassVar[list] = []

    def __init__(self):
        self.METHODS: dict[str, Callable[[], dict[str, Any]]] = {
            PaylovMethods.CHECK_TRANSACTION: self.check_transaction,
            PaylovMethods.PERFORM_TRANSACTION: self.perform_transaction,
        }
        self.params: dict[str, Any] | None = None
        super().__init__()

    def post(self, request, *args, **kwargs) -> Response:
        is_authenticated = paylov_authentication(request)
        if not is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        print(">>> Request data: ", request.data)

        serializer = PaylovSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        method = serializer.validated_data["method"]
        self.params = serializer.validated_data["params"]

        with db_transaction.atomic():
            response_data = self.METHODS[method]()

        if isinstance(response_data, dict):
            response_data.update({"jsonrpc": "2.0", "id": request.data.get("id", None)})

        return Response(response_data)

    def check_transaction(self) -> dict[str, Any]:
        error, code = PaylovClient(self.params).check_transaction()

        if error:
            if code == STATUS_CODES["ORDER_NOT_FOUND"]:
                return dict(result=dict(status=code, statusText=STATUS_TEXT["ERROR"]))
            elif code == STATUS_CODES["INVALID_AMOUNT"]:
                return dict(result=dict(status=code, statusText=STATUS_TEXT["ERROR"]))
        return dict(result=dict(status=code, statusText=STATUS_TEXT["SUCCESS"]))

    def perform_transaction(self) -> dict[str, Any]:
        error, code = PaylovClient(self.params).perform_transaction()

        if error and code == STATUS_CODES["ORDER_NOT_FOUND"]:
            return dict(result=dict(status=code, statusText=STATUS_TEXT["ERROR"]))

        provider = Providers.objects.filter(key="paylov").last()
        print(provider)
        transaction = Transaction.objects.get(
            id=self.params["account"]["order_id"],
            provider=provider,
        )

        if error:
            transaction.status = TransactionStatus.FAILED
            transaction.save(update_fields=["status"])
            return dict(result=dict(status=code, statusText=STATUS_TEXT["ERROR"]))

        transaction.apply_transaction(provider=provider, transaction_id=self.params['transaction_id'])
        return dict(result=dict(status=code, statusText=STATUS_TEXT["SUCCESS"]))


_all_ = ['PaylovAPIView']
