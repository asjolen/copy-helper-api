from django.urls import path
from organization.views.organization import OrganizationView
from organization.views.invite import InviteView

urlpatterns = [
    path('organization/', OrganizationView.as_view()),
    path('invite/', InviteView.as_view()),
]