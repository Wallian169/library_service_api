from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
)

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingCreateSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
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

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
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
