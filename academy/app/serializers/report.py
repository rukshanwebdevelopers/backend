from academy.app.serializers.base import BaseSerializer
from academy.app.serializers.course import CourseOfferingLiteSerializer
from academy.app.serializers.student import StudentListSerializer
from academy.db.models import Enrollment


class PendingPaymentListSerializer(BaseSerializer):
    student = StudentListSerializer()
    course_offering = CourseOfferingLiteSerializer()

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'status',
            'last_payment_month',
            'last_payment_year',
            'is_active',
            'student',
            'course_offering',
        ]
