# Third party imports
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import ROLE
from academy.app.serializers.coodinator import CoordinatorSerializer, CoordinatorListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import User


class CoordinatorViewSet(BaseViewSet):
    model = User
    serializer_class = CoordinatorListSerializer

    search_fields = ["username", "email"]
    ordering_fields = ['first_name', 'created_at']

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().filter(role=ROLE.COORDINATOR.value))
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CoordinatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        coordinator = serializer.save()

        output = self.serializer_class(coordinator, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        coordinator = User.objects.get(pk=kwargs["pk"])

        serializer = CoordinatorSerializer(
            coordinator,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        coordinator = serializer.save()

        output = self.serializer_class(coordinator, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)
