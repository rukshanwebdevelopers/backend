from django.db import models

from core.models.base import BaseModel


# Create your models here.
class Subject(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)

    class Meta:
        db_table = "subject"

    def __str__(self):
        return self.name
