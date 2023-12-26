import json

from decimal import Decimal

from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.db.models import Q
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Sector, Course
from .serializers import SectorSerializer, CourseUnpaidSerializer, CourseListSerializer, CommentSerializer, CartItemSerializer, CoursePaidSerializer
from core.utils import get_object_or_none
from django.contrib.auth import get_user_model

User = get_user_model()


class SectorsHomeView(APIView):

    def get(self, request, *args, **kwargs):
        sectors = Sector.objects.order_by('?')[:6]
        sector_response = SectorSerializer(sectors, many=True).data

        return Response(data=sector_response, status=status.HTTP_200_OK)


class CourseDetail(APIView):
    def get(self, request, course_uuid, *args, **kwargs):
        course = get_object_or_none(Course, course_uuid=course_uuid)
        if not course:
            return HttpResponseBadRequest('Course does not exist')
        serializer = CourseUnpaidSerializer(course)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SectorCourse(APIView):
    def get(self, request, sector_uuid, *args, **kwargs):
        sector = get_object_or_none(Sector, sector_uuid=sector_uuid)
        if not sector:
            return HttpResponseBadRequest("Sector does not exist")
        sector_courses = sector.related_courses.all()
        serializer = CourseListSerializer(sector_courses, many=True)
        total_students = 0
        for course in sector_courses:
            total_students += course.user_set.all().count()

        return Response({'data': serializer.data, 'sector_name': sector.name, 'total_students': total_students}, status=status.HTTP_200_OK)


class SearchCourse(APIView):
    def get(self, request, search_term, *args, **kwargs):
        matches = Course.objects.filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term))
        serializer = CourseListSerializer(matches, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AddComment(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, course_uuid, *args, **kwargs):
        course = get_object_or_none(Course, course_uuid=course_uuid)
        if not course:
            return HttpResponseBadRequest("Course does not exist")

        if not request.data.get('message'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        comment = serializer.save(user=request.user)
        course.comments.add(comment)

        return Response(status=status.HTTP_201_CREATED)


class GetCartDetail(APIView):

    def post(self, request, *args, **kwargs):
        cart = request.data.get('cart')
        if not isinstance(cart, list):
            return HttpResponseBadRequest()
        if len(cart) == 0:
            return Response([])
        courses = Course.objects.filter(course_uuid__in=cart)

        serializer = CartItemSerializer(courses, many=True)
        cart_total = sum(courses.values_list('price', flat=True))
        return Response({'cart_detail': serializer.data, 'cart_total': cart_total}, status=status.HTTP_200_OK)


class CourseStudy(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_uuid):
        course = get_object_or_none(Course, course_uuid=course_uuid)
        if not course:
            return HttpResponseBadRequest("Course does not exist")
        request.user = User.objects.get(id=1)

        if course not in request.user.paid_courses.all():
            return HttpResponseForbidden("User is not enrolled to this course")
        serializer = CoursePaidSerializer(course)

        return Response(serializer.data, status=status.HTTP_200_OK)
