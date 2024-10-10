from django.contrib.auth import get_user_model
from django.db import models

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
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
