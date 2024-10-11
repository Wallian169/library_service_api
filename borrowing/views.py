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
    queryset = Borrowing.objects.select_related("book_id")
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
        queryset = self.queryset
        if self.action == "list":
            if self.request.user.is_superuser:
                return queryset
            queryset = queryset.filter(user_id=self.request.user)
        return queryset
