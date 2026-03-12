from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.video import VideoListSerializer, VideoCreateSerializer, VideoUpdateSerializer
from academy.app.views.base import BaseViewSet, BaseAPIView
from academy.db.models import Video


# Create your views here.
class VideoListCreateAPIEndpoint(BaseViewSet):
    """Video List and Create Endpoint"""

    model = Video
    serializer_class = VideoListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        serializer = VideoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        video = serializer.save()

        output = self.serializer_class(video, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)


class VideoDetailAPIEndpoint(BaseAPIView):
    """Video Endpoints to update, retrieve and delete endpoint"""

    model = Video
    serializer_class = VideoListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            Video.objects.filter(id=self.kwargs['pk'])
            .distinct()
        )

    def get(self, request, *args, pk):
        """Retrieve video

        Retrieve details of a specific project.
        """
        course_content = self.get_queryset().get(pk=pk)
        serializer = self.serializer_class(course_content)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Update course content

        Partially update an existing course content's properties like name, description, or settings.
        Tracks changes in model activity logs for audit purposes.
        """
        try:
            video = Video.objects.get(pk=pk)

            serializer = VideoUpdateSerializer(
                video,
                data={**request.data},
                partial=True,
            )

            if serializer.is_valid():
                serializer.save()

                video = self.get_queryset().filter(pk=serializer.instance.id).first()

                serializer = VideoListSerializer(video)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"name": "The project name is already taken"},
                    status=status.HTTP_409_CONFLICT,
                )
