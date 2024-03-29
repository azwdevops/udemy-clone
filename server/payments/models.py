from django.db import models

from users.models import User
from courses.models import Course


class PaymentIntent(models.Model):
    payment_intent_id = models.CharField(max_length=255)
    checkout_id = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    payment_intent = models.ForeignKey(PaymentIntent, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
