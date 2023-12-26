from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from .models import Sector, Course, Comment, CourseSection, Episode
from users.serializers import UserSerializer


class SectorSerializer(ModelSerializer):
    featured_courses = SerializerMethodField('get_featured_courses')
    sector_image = serializers.CharField(source='get_image_absolute_url')

    class Meta:
        model = Sector
        fields = ['name', 'sector_uuid', 'featured_courses', 'sector_image']

    def get_featured_courses(self, obj):
        return CourseDisplaySerializer(obj.related_courses.order_by('?')[:4], many=True).data


class CourseDisplaySerializer(ModelSerializer):
    student_no = serializers.IntegerField(source='get_enrolled_students')
    image_url = serializers.CharField(source='get_image_absolute_url')
    author = UserSerializer()

    class Meta:
        model = Course
        fields = ['title', 'course_uuid', 'price',
                  'student_no', 'image_url', 'author']


class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['id']


class EpisodeUnpaidSerializer(ModelSerializer):
    length = serializers.CharField(source='get_video_length_time')

    class Meta:
        model = Episode
        exclude = ['file']


class EpisodePaidSerializer(ModelSerializer):
    length = serializers.CharField(source='get_video_length_time')

    class Meta:
        model = Episode
        fields = ['file', 'length', 'title']


class CourseSectionUnpaidSerializer(ModelSerializer):
    episodes = EpisodeUnpaidSerializer(many=True)
    total_duration = serializers.CharField(source='total_length')

    class Meta:
        model = CourseSection
        fields = ['section_title', 'episodes', 'total_duration']


class CourseSectionPaidSerializer(ModelSerializer):
    episodes = EpisodePaidSerializer(many=True)
    total_duration = serializers.CharField(source='total_length')

    class Meta:
        model = CourseSection
        fields = ['section_title', 'episodes', 'total_duration']


class CourseUnpaidSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)
    author = UserSerializer()
    course_sections = CourseSectionUnpaidSerializer(many=True)
    student_no = serializers.IntegerField(source='get_enrolled_students')
    total_lectures = serializers.IntegerField(source='get_total_lectures')
    total_duration = serializers.CharField(source='total_course_length')
    image_url = serializers.CharField(source='get_image_absolute_url')

    class Meta:
        model = Course
        exclude = ['id']


class CoursePaidSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)
    author = UserSerializer()
    course_sections = CourseSectionPaidSerializer(many=True)
    student_no = serializers.IntegerField(source='get_enrolled_students')
    total_lectures = serializers.IntegerField(source='get_total_lectures')
    total_duration = serializers.CharField(source='total_course_length')
    image_url = serializers.CharField(source='get_image_absolute_url')

    class Meta:
        model = Course
        exclude = ['id']


class CourseListSerializer(ModelSerializer):
    image_url = serializers.CharField(source='get_image_absolute_url')
    total_lectures = serializers.IntegerField(source='get_total_lectures')
    student_no = serializers.IntegerField(source='get_enrolled_students')
    description = serializers.CharField(source='get_brief_description')
    author = UserSerializer()

    class Meta:
        model = Course
        fields = ['title', 'course_uuid', 'price',
                  'total_lectures', 'author', 'description', 'student_no', 'image_url']


class CartItemSerializer(ModelSerializer):
    author = UserSerializer()
    image_url = serializers.CharField(source='get_image_absolute_url')

    class Meta:
        model = Course
        fields = ['author', 'title', 'price', 'image_url']
