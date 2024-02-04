from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    isAdmin = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'isAdmin', 'name']

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        try:
            name = str(obj.first_name + " " +obj.last_name)
            name = name.title()
        except:
            name = obj.username

        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class CourseSerializer(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'numOfLikes', 'watches', 'image', 'lectures']

    def get_lectures(self, obj):
        lectures = Lecture.objects.filter(course_id=obj.id)
        serializers = LectureSerializer(lectures, many=True)
        return serializers.data

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

