# Third party imports
from rest_framework import serializers

# Module imports
from academy.db.models import Video, CourseContent
from .base import BaseSerializer


class VideoCreateSerializer(BaseSerializer):
    """
    Serializer for creating video with course content validation and date checking.
    """

    month = serializers.IntegerField()
    year = serializers.IntegerField()
    course_offering_id = serializers.UUIDField()

    class Meta:
        model = Video
        fields = [
            'title',
            'video_url',
            'month',
            'year',
            'course_offering_id',
        ]

    def create(self, validated_data):
        month = validated_data.pop('month')
        year = validated_data.pop('year')
        course_offering_id = validated_data.pop('course_offering_id')

        course_content, created = CourseContent.objects.get_or_create(
            month=month,
            year=year,
            course_offering_id=course_offering_id,
        )

        video = Video.objects.create(
            **validated_data,
            course_content=course_content
        )

        return video


class VideoUpdateSerializer(BaseSerializer):
    """
    Serializer for updating video.
    """

    class Meta:
        model = Video
        fields = [
            'title',
            'video_url',
        ]


class VideoListSerializer(BaseSerializer):
    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'video_url',
        ]
