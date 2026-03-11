from crum import get_current_user
from rest_framework import status
from rest_framework.response import Response

from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.conversation import ConversationListSerializer, ConversationSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Conversation


# Create your views here.
class ConversationViewSet(BaseViewSet):
    model = Conversation
    serializer_class = ConversationListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        current_user = get_current_user()

        return (
            self.filter_queryset(
                super()
                .get_queryset()
                .filter(participants__user=current_user)
                # .select_related("latest_message")
                .prefetch_related("participants__user")
                .distinct()
            )
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
