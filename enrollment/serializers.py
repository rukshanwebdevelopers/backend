from core.serializers.base import BaseSerializer
from enrollment.models import Enrollment, EnrollmentStatusType


class EnrollmentSerializer(BaseSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['status']

    def create(self, validated_data):
        validated_data['status'] = EnrollmentStatusType.LOCKED
        return super().create(validated_data)


class EnrollmentListSerializer(BaseSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
