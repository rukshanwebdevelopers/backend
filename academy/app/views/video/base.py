# Django imports
from django.db import IntegrityError
# Third-part imports
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course_content import VideoCreateSerializer, VideoListSerializer, VideoUpdateSerializer, \
    VideoLiteSerializer
from academy.app.views.base import BaseViewSet, BaseAPIView
from academy.db.models import Video


# Create your views here.
class VideoListCreateAPIEndpoint(BaseViewSet):
    """Video List and Create Endpoint"""

    model = Video
    serializer_class = VideoListSerializer

    search_fields = ['title']
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
            .select_related('course_content',
                            'course_content__course_offering',
                            'course_content__course_offering__course',
                            'course_content__course_offering__course__subject',
                            )
        )

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        serializer = VideoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        video = serializer.save()

        output = VideoLiteSerializer(video, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)


class VideoDetailAPIEndpoint(BaseAPIView):
    """Video Endpoints to update, retrieve and delete endpoint"""

    model = Video
    serializer_class = VideoListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return Video.objects.all()

    @allow_permission([ROLE.ADMIN])
    def get(self, request, *args, pk):
        """Retrieve video

        Retrieve details of a specific video.
        """
        video = (self.get_queryset()
                 .select_related('course_content',
                                 'course_content__course_offering',
                                 'course_content__course_offering__course',
                                 'course_content__course_offering__course__subject',
                                 )
                 .get(pk=pk))
        serializer = self.serializer_class(video)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def patch(self, request, pk):
        """Update video"""
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

                serializer = VideoLiteSerializer(video)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"name": "The project name is already taken"},
                    status=status.HTTP_409_CONFLICT,
                )

    @allow_permission([ROLE.ADMIN])
    def delete(self, request, pk):
        """Delete video"""
        video = self.get_queryset().filter(pk=pk)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
