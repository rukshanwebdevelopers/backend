from core.serializers.base import BaseSerializer
from guardian.models import Guardian


class GuardianSerializer(BaseSerializer):
    class Meta:
        model = Guardian
        fields = '__all__'


class GuardianListSerializer(BaseSerializer):
    class Meta:
        model = Guardian
        fields = '__all__'
