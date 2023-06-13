from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from users.models import CustomUser

# Create your models here.


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_isbn = models.CharField(max_length=50)

    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stars_given} stars for {self.book_isbn} by {self.user.username}"
