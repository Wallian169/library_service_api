from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowing.models import Borrowing

BORROWING_URL = reverse("borrowing:borrowing-list")


def sample_book(**params):
    """Create and return a sample book."""
    defaults = {
        "title": "Sample Book",
        "author": "Sample Author",
        "cover": "Hard",
        "daily_fee": Decimal("1.50"),
        "inventory": 5,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class UnauthenticatedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access the borrowing list."""
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@library.com", password="pass24word"
        )
        self.second_user = get_user_model().objects.create_user(
            email="second_user@library.com", password="secondpass"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin_user@library.com",
            password="adminpass332",
        )
        self.client.force_authenticate(self.user)
        self.book1 = sample_book(
            title="Sample Book1",
            author="Sample Author2",
            cover="Hard",
            daily_fee=Decimal("1.50"),
            inventory=2,
        )
        self.book2 = sample_book(
            title="Sample Book2",
            author="Sample Author3",
            cover="Hard",
            daily_fee=Decimal("1.50"),
            inventory=2,
        )
        self.borrowing_data = {
            "book_id": self.book1.id,
            "expected_return_date": date.today() + timedelta(days=7),
        }
        self.borrowing1 = Borrowing.objects.create(
            user_id=self.user,
            book_id=self.book1,
            actual_return_date=None,
            expected_return_date=date.today() + timedelta(days=7),
        )
        self.borrowing2 = Borrowing.objects.create(
            user_id=self.user,
            book_id=self.book2,
            actual_return_date=None,
            expected_return_date=date.today() + timedelta(days=7),
        )
        self.borrowing3 = Borrowing.objects.create(
            user_id=self.user,
            book_id=self.book1,
            actual_return_date="2024-01-01",
            expected_return_date=date.today() + timedelta(days=7),
        )
        self.borrowing4 = Borrowing.objects.create(
            user_id=self.second_user,
            book_id=self.book2,
            expected_return_date=date.today() + timedelta(days=7),
            actual_return_date=None,
        )

    def test_auth(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrowing_creation(self):
        """Test that authenticated users can create a borrowing record."""
        response = self.client.post(BORROWING_URL, self.borrowing_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_return_borrowing(self):
        url = reverse(
            "borrowing:borrowing-return-borrowing", kwargs={"pk": self.borrowing1.id}
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.borrowing1.refresh_from_db()
        self.book1.refresh_from_db()

        self.assertEqual(self.book1.inventory, 3)

    def test_filter_borrowings_by_is_active(self):
        """Test filtering for active/inactive borrowings"""
        response = self.client.get(
            reverse("borrowing:borrowing-list"), {"is_active": "true"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertNotIn(
            self.borrowing3.id, [borrowing["id"] for borrowing in response.data]
        )

    def test_other_user_borrowing_unlisted(self):
        response = self.client.get(reverse("borrowing:borrowing-list"))
        self.assertEqual(len(response.data), 3)
        self.assertNotIn(
            self.borrowing4.id, [borrowing["id"] for borrowing in response.data]
        )

    def test_listed_all_for_admin(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(reverse("borrowing:borrowing-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_admin_filter_by_user_id(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(
            reverse("borrowing:borrowing-list"), {"user_id": self.second_user.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
