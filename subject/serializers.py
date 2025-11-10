from core.serializers.base import BaseSerializer
from subject.models import Subject


class SubjectSerializer(BaseSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class SubjectListSerializer(BaseSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug', 'code']
