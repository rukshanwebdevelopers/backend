from rest_framework import status
from rest_framework.response import Response

from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course_content import VideoListSerializer, VideoLiteSerializer
from academy.app.views.base import BaseAPIView
from academy.db.models import Student, Video


class StudentWatchVideoEndpoint(BaseAPIView):
    @allow_permission([ROLE.STUDENT])
    def get(self, request, *args, pk):
        user = request.user

        student = Student.objects.get(user=user)

        # Get all courses the student is enrolled in
        video = Video.objects.get(pk=pk)

        output = VideoLiteSerializer(video).data
        return Response(output, status=status.HTTP_200_OK)
