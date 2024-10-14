from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from books.models import Book


class BookUnauthorizedTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book", author="<NAME>", cover="Hard", daily_fee=Decimal("1.50")
        )

    def test_unauthorized_list(self):
        """Book list should have unauthorized access"""
        response = self.client.get(reverse("books:books-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_detail(self):
        response = self.client.get(
            reverse("books:books-detail", kwargs={"pk": self.book.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
