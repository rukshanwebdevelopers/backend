from django.db import models

from authentication.models import User
from core.models.base import BaseModel
from subject.models import Subject


# Create your models here.
class Course(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    fee = models.FloatField()

    subject = models.ForeignKey(
        Subject,
        related_name="courses",
        on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        User,
        related_name="courses",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "course"

    def __str__(self):
        return self.name
