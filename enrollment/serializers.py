from django.utils import timezone
from rest_framework import serializers

from core.serializers.base import BaseSerializer
from course.serializers import CourseListSerializer
from enrollment.models import Enrollment, EnrollmentStatusType, EnrollmentPayment
from user.serializers import StudentListSerializer


class EnrollmentSerializer(BaseSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['status']

    def create(self, validated_data):
        validated_data['status'] = EnrollmentStatusType.LOCKED
        validated_data['is_active'] = True
        return super().create(validated_data)


class EnrollmentListSerializer(BaseSerializer):
    student = StudentListSerializer()
    course = CourseListSerializer()

    class Meta:
        model = Enrollment
        fields = '__all__'


class EnrollmentPaymentSerializer(BaseSerializer):
    class Meta:
        model = EnrollmentPayment
        fields = '__all__'


class EnrollmentPaymentCreateSerializer(BaseSerializer):
    student = serializers.UUIDField(write_only=True)
    course = serializers.UUIDField(write_only=True)

    class Meta:
        model = EnrollmentPayment
        fields = '__all__'
        read_only_fields = ['payment_date', 'enrollment']

    def validate(self, attrs):
        student = attrs.get("student")
        course = attrs.get("course")

        enrollment = Enrollment.objects.filter(
            student=student,
            course=course,
        ).first()

        if not enrollment:
            raise serializers.ValidationError(
                {"course": "Student not enrolled to this course"}
            )

        # save enrollment into serializer instance
        attrs["enrollment"] = enrollment

        # Check duplicate payment
        if EnrollmentPayment.objects.filter(
            enrollment=enrollment,
            payment_month=attrs["payment_month"],
            payment_year=attrs["payment_year"],
        ).exists():
            raise serializers.ValidationError(
                {"payment_month": "Already paid for this course"}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("student", None)
        validated_data.pop("course", None)

        # automatic payment date
        validated_data["payment_date"] = timezone.now().date()

        return EnrollmentPayment.objects.create(**validated_data)


class EnrollmentPaymentListSerializer(BaseSerializer):
    enrollment = EnrollmentListSerializer()

    class Meta:
        model = EnrollmentPayment
        fields = '__all__'
