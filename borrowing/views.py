from django.db import transaction
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingCreateSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
)


class BorrowingViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book_id").order_by(
        "actual_return_date"
    )
    serializer_class = BorrowingListSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: BorrowingReturnSerializer},
        description="Return a borrowed book and update its inventory.",
    )
    @action(detail=True, methods=["POST"], url_path="return")
    @transaction.atomic
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            raise ValidationError("The borrowing has already been returned.")

        borrowing.actual_return_date = timezone.now().date()
        borrowing.save()

        book = borrowing.book_id
        book.inventory += 1
        book.save()

        serializer = BorrowingReturnSerializer(borrowing)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.STR,
                description="Filter by status of borrowings (ex. ?is_active=true)",
            ),
            OpenApiParameter(
                "user_id",
                type=OpenApiTypes.INT,
                description=(
                    "Filter borrowings by concrete user via id " "(ex. ?user_id=2)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "return_borrowing":
            return BorrowingReturnSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")
        queryset = self.queryset

        if self.action == "list":
            if not self.request.user.is_superuser:
                queryset = queryset.filter(user_id=self.request.user)
            else:
                if user_id:
                    queryset = queryset.filter(user_id=user_id)

            if is_active and is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)

        return queryset
