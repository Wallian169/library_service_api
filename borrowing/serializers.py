from rest_framework import serializers

from books.models import Book
from books.serializers import BookInBorrowingSerializer, BookListSerializer
from borrowing.models import Borrowing


class BorrowingCreateSerializer(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    borrow_date = serializers.DateField(read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "book_id")

    def create(self, validated_data):
        book = validated_data["book_id"]

        if book.inventory <= 0:
            raise serializers.ValidationError("Book is not available")

        book.inventory -= 1
        book.save()

        return super().create(validated_data)


class BorrowingListSerializer(serializers.ModelSerializer):
    book_info = BookListSerializer(read_only=True, source="book_id")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_info",
        )


class BorrowingDetailSerializer(BorrowingListSerializer):
    book_info = BookInBorrowingSerializer(source="book_id", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_info",
        )
