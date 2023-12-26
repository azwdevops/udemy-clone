from decimal import Decimal

from django.db import transaction


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseBadRequest
from rest_framework import status
import stripe
from decouple import config
from core.utils import get_object_or_none

from courses.models import Course
from .models import PaymentIntent, Payment

from decouple import config

stripe.api_key = config("STRIPE_API_KEY")
endpoint_secret = config('STRIPE_SECRET')


class PaymentHandler(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        if not isinstance(request.data, list) or len(request.data) == 0:
            return HttpResponseBadRequest("You must specify the courses")

        course_line_items = []
        courses = Course.objects.filter(course_uuid__in=request.data)
        for course_item in courses:
            line_item = {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(course_item.price * 100),
                    "product_data": {
                        "name": course_item.title
                    },
                },
                "quantity": 1
            }
            course_line_items.append(line_item)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=course_line_items,
            mode="payment",
            success_url=config("SITE_URL"),
            cancel_url=config("SITE_URL"),
        )
        intent = PaymentIntent.objects.create(
            payment_intent_id=checkout_session.payment_intent,
            checkout_id=checkout_session.id,
            user=request.user
        )
        intent.courses.add(*courses)

        return Response({"url": checkout_session.url}, status=status.HTTP_200_OK)


class Webhook(APIView):
    @transaction.atomic
    def post(self, request):
        payload = request.data
        # verify request is coming from stripe and not another source
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=endpoint_secret
            )
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            intent = get_object_or_none(
                PaymentIntent, checkout_id=session.id, payment_intent_id=session.payment_intent)
            if not intent:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Payment.objects.create(
                payment_intent=intent, total_amount=Decimal(session.amount_total / 100))
            intent.user.paid_courses.add(*(intent.courses.all()))
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
