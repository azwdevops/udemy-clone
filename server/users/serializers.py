from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['name']


class UserAuthSerializer(ModelSerializer):
    courses = serializers.ListField(source='get_all_courses')

    class Meta:
        model = User
        fields = ['email', 'id', 'name', 'courses']
