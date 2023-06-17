from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    def __str__(self) -> str:
        return self.username

    per_day = models.DecimalField(max_digits=16, decimal_places=2, default=0)


class Entry(models.Model):
    class Meta:
        verbose_name_plural = "Entries"

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="entries")
    name = models.CharField(max_length=255)
    number = models.DecimalField(max_digits=16, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    expected = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "expected": self.expected,
        }
