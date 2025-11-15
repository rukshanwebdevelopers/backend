from django.db import models

from core.models.base import BaseModel
from course.models import Course
from user.models import Student


# Create your models here.
class EnrollmentStatusType(models.TextChoices):
    ACTIVE = "ACTIVE"
    LOCKED = "LOCKED"


class Enrollment(BaseModel):
    status = models.CharField(max_length=20, choices=EnrollmentStatusType.choices)
    last_payment_month = models.PositiveIntegerField(default=0)
    last_payment_year = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    student = models.ForeignKey(
        Student,
        related_name="enrollments",
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        related_name="enrollments",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "enrollment"

    def __str__(self):
        return self.status


class EnrollmentPayment(BaseModel):
    payment_month = models.PositiveIntegerField(default=0)
    payment_year = models.PositiveIntegerField(default=0)
    amount = models.FloatField()
    payment_date = models.DateField()

    enrollment = models.ForeignKey(
        Enrollment,
        related_name="enrollment_payments",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "enrollment_payment"

    def __str__(self):
        return self.payment_month
