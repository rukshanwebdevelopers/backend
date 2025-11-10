from django.db import models

from core.models.base import BaseModel


# Create your models here.
class Guardian(BaseModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nic_number = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=10)
    gender = models.FloatField()

    class Meta:
        db_table = "guardian"

    def __str__(self):
        return self.first_name
