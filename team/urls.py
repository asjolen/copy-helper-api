from django.urls import path
from team.views.team import TeamView

urlpatterns = [
    path('team/', TeamView.as_view()),
]