from django.urls import path
from user.views.user import UserView

urlpatterns = [
    path('user/', UserView.as_view()),
]