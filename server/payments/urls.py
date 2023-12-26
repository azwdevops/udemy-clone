from django.urls import path

from . import views

urlpatterns = [
    path('payment-handler/', views.PaymentHandler.as_view(), name='payment_handler'),
    path('webhook/', views.Webhook.as_view(), name='webhook'),
]
