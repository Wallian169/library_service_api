from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from books.models import Book
from books.serializers import BookSerializer, BookListSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(BookViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return self.serializer_class
