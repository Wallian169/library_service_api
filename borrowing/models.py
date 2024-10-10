from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from rest_framework.exceptions import ValidationError

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True, default=None)
    book_id = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
        db_column="book_id",
    )
    user_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="borrowings",
        db_column="user_id",
    )

    def clean(self):
        if self.expected_return_date <= timezone.now().date():
            raise ValidationError("Expected return date must be in the future.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Borrowing, self).save(*args, **kwargs)
