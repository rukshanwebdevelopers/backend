# Third party imports
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.user import UserListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import User


class UserViewSet(BaseViewSet):
    model = User
    serializer_class = UserListSerializer

    search_fields = ["username", "email"]
    ordering_fields = ['first_name', 'is_active', 'created_at']

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def deactivate(self, request, *args, **kwargs):
        deactivate_user_id = request.data['id']
        user = User.objects.get(id=deactivate_user_id)

        # Deactivate the user
        user.is_active = False
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
