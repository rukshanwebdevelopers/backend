from rest_framework import serializers

from academy.app.permissions.base import ROLE
from academy.app.serializers.academic_year import AcademicYearListSerializer
from academy.app.serializers.grade_level import GradeLevelListSerializer
from academy.app.serializers.user import UserLiteSerializer
from academy.db.models import Student, User


class StudentListSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()
    current_grade = GradeLevelListSerializer()
    current_academic_year = AcademicYearListSerializer()

    class Meta:
        model = Student
        fields = [
            'id',
            'student_number',
            'date_of_birth',
            'gender',
            'is_active',
            'user',
            'current_grade',
            'current_academic_year',
            'parent_guardian_name',
            'parent_guardian_phone'
        ]


class StudentCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    parent_guardian_phone = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["student_number", "user"]

    # --- VALIDATION ---
    # def validate_username(self, value):
    #     if User.objects.filter(username=value).exists():
    #         raise serializers.ValidationError("Username already exists.")
    #     return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    # --- CREATE ---
    def create(self, validated_data):
        # Extract fields NOT in Student model
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        username = validated_data.pop("username", None)
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # Create user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            role=ROLE.STUDENT.value,
        )
        user.set_password(password)
        user.save()

        # Now validated_data ONLY contains Student model fields
        student = Student.objects.create(user=user, **validated_data)
        return student


class StudentUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    parent_guardian_phone = serializers.CharField(write_only=True)
    # password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["student_number", "user"]

    # --- VALIDATION ---
    def validate_username(self, value):
        user = self.instance.user
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value

    def validate_email(self, value):
        user = self.instance.user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    # --- UPDATE ---
    def update(self, instance, validated_data):
        """
        instance → Student instance
        instance.user → related User instance
        validated_data → student fields + username/email/password
        """

        user = instance.user

        # Extract user fields
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        username = validated_data.pop("username", None)
        email = validated_data.pop("email", None)
        # password = validated_data.pop("password", None)

        # Update User fields
        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if username:
            user.username = username

        if email:
            user.email = email

        # if password:
        #     user.set_password(password)

        user.save()

        # Update Student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class StudentLiteSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()
    current_grade = GradeLevelListSerializer()
    current_academic_year = AcademicYearListSerializer()

    class Meta:
        model = Student
        fields = [
            'id',
            'student_number',
            'date_of_birth',
            'gender',
            'is_active',
            'user',
            'current_grade',
            'current_academic_year',
            'parent_guardian_name',
            'parent_guardian_phone'
        ]
