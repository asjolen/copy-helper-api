from django.urls import path
from subscription.views.usage import SubscriptionUsageView

urlpatterns = [
    path('usage/', SubscriptionUsageView.as_view()),
]