from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.models import Transaction, UserCard
from apps.payment.paylov.client import PaylovClient
from apps.payment.serializers.card import (
    AddCardSerializer,
    ConfirmCardSerializer,
    DeleteCardSerializer,
    CardReceiptCreateSerializer,
    CardReceiptConfirmSerializer
)


class AddCardAPIView(APIView):
    serializer_class = AddCardSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AddCardSerializer,
        responses={200: "Success", 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        _, response = PaylovClient().create_user_card(
            user=request.user,
            card_number=serializer.validated_data["card_number"],
            expire_month=serializer.validated_data["exp_month"],
            expire_year=serializer.validated_data["exp_year"],
        )

        return Response(data=response, status=status.HTTP_200_OK)


class ConfirmUserCardAPIView(APIView):
    serializer_class = ConfirmCardSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ConfirmCardSerializer,
        responses={200: "Success", 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        _, response = PaylovClient().confirm_user_card(
            user=request.user,
            card_id=serializer.validated_data["card_id"],
            otp=serializer.validated_data["otp"],
            card_name=serializer.validated_data["card_name"],
        )

        return Response(data=response, status=status.HTTP_200_OK)


class DeleteUserCardAPIView(APIView):
    serializer_class = DeleteCardSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=DeleteCardSerializer,
        responses={200: "Success", 400: "Validation Error"},
    )
    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        _, response = PaylovClient().delete_user_card(
            card_id=serializer.validated_data("card_id")
        )

        return Response(data=response, status=status.HTTP_200_OK)


class GetSingleUserCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        _, response = PaylovClient().get_single_card(card_id=kwargs.get("card_id"))

        return Response(data=response, status=status.HTTP_200_OK)


class ListUserCardsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print(">>>", args, kwargs)
        _, response = PaylovClient().get_user_cards(user_id=kwargs["user_id"])

        return Response(data=response, status=status.HTTP_200_OK)


class UserCardReceiptCreateAPIView(APIView):
    serializer_class = CardReceiptCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CardReceiptCreateSerializer,
        responses={200: "Success", 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_token = serializer.validated_data["card_token"]
        product_id = serializer.validated_data["product_id"]
        product_type = serializer.validated_data["product_type"]

        _, response = PaylovClient().create_receipt(
            user=request.user,
            card_token=card_token,
            product_id=product_id,
            product_type=product_type,
        )

        return Response(data=response, status=status.HTTP_200_OK)


class UserCardReceiptConfirmAPIView(APIView):
    serializer_class = CardReceiptConfirmSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CardReceiptConfirmSerializer,
        responses={200: "Success", 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_id = serializer.validated_data["transaction_id"]
        transaction = Transaction.objects.filter(remote_id=transaction_id).first()
        card_token = serializer.validated_data["card_token"]
        card = UserCard.objects.filter(card_token=card_token).first()

        if not card:
            return Response(
                data={"detail": "User card not found", "code": "card_not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        _, response = PaylovClient().pay_receipt(
            user_id=request.user.id,
            transaction=transaction,
            card=card,
        )

        return Response(data=response, status=status.HTTP_200_OK)


_all_ = ['AddCardAPIView', 'ConfirmUserCardAPIView', 'DeleteUserCardAPIView', 'GetSingleUserCardAPIView',
         'ListUserCardsAPIView', 'UserCardReceiptCreateAPIView', 'UserCardReceiptConfirmAPIView']
