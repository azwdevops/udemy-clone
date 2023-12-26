from django.contrib import admin

from .models import PaymentIntent, Payment

admin.site.register(Payment)
admin.site.register(PaymentIntent)
