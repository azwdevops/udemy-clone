from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from decouple import config
from decimal import Decimal
from mutagen.mp4 import MP4, MP4StreamInfoError

from core.utils import get_timer

User = get_user_model()


class Sector(models.Model):
    name = models.CharField(max_length=255)
    sector_uuid = models.UUIDField(
        default=uuid4, editable=False, unique=True)
    related_courses = models.ManyToManyField('Course', blank=True)
    sector_image = models.ImageField(upload_to='sector_images')

    def __str__(self):
        return self.name

    def get_image_absolute_url(self):
        return config('SITE_URL') + self.sector_image.url


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    course_sections = models.ManyToManyField('CourseSection', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    image_url = models.ImageField(upload_to='course_images')
    course_uuid = models.UUIDField(
        default=uuid4, editable=False, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    def get_brief_description(self):
        return self.description[:100]

    def get_enrolled_students(self):
        return User.objects.filter(paid_courses=self).count()

    def get_total_lectures(self):
        lectures = 0
        for section in self.course_sections.all():
            lectures += section.episodes.all().count()
        return lectures

    def total_course_length(self):
        length = Decimal(0.0)
        for section in self.course_sections.all():
            length += sum(section.episode.all().values_list('length', flat=True))
        return get_timer(length, type='short')

    def get_image_absolute_url(self):
        return config('SITE_URL') + self.image_url.url


class CourseSection(models.Model):
    section_title = models.CharField(max_length=255)
    episodes = models.ManyToManyField('Episode', blank=True)

    def total_length(self):
        total = sum(self.episodes.all().values_list('length'))

        return get_timer(total, type='min')

    def __str__(self):
        return self.section_title


class Episode(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_videos')
    length = models.DecimalField(max_digits=10, decimal_places=2)

    def get_video_length(self):
        try:
            video = MP4(self.file)
            return video.info.length
        except MP4StreamInfoError:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)

    def get_absolute_url(self):
        return config('SITE_URL') + self.file.url

    def save(self, *args, **kwargs):
        self.length = self.get_video_length()
        return super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
