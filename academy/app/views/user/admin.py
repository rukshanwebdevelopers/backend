from academy.app.permissions.base import ROLE, allow_permission
from academy.app.serializers.user import UserListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import User


class AdminViewSet(BaseViewSet):
    model = User
    serializer_class = UserListSerializer

    search_fields = ["username", "email"]

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().filter(role=ROLE.ADMIN.value))
        )

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
