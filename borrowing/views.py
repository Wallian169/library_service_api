from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingCreateSerializer, BorrowingListSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return self.serializer_class


    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
