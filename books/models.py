from enum import Enum

from django.db import models


class Book(models.Model):
    class CoverType(Enum):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4,
        choices=[(tag.name, tag.value) for tag in CoverType],
    )
    inventory = models.PositiveSmallIntegerField(default=1)
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title
