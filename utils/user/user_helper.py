from django.contrib.auth import authenticate
from team.models import Team, Member as TeamMember
from team.serializers import TeamSerializer
from organization.models import Organization, Member as OrganizationMember
from organization.serializers import OrganizationSerializer
import requests
import os


class UserHelper:
    ORGANIZATION_MEMBER = 0
    ORGANIZATION_MANAGER = 10
    TEAM_MEMBER = 0
    TEAM_MANAGER = 10

    def authenticated_user(self, request):
        return authenticate(remote_user=request.user.id)

    def fetch_user(self, request):
        result = requests.get(
            "https://" + os.environ.get("AUTH0_DOMAIN") + "/userinfo",
            headers={
                "Authorization": request.headers["Authorization"]
            }
        )

        if result.status_code == 200:
            return {
                "result": result.json(),
                "status": result.status_code
            }
        else:
            return {
                "status": result.status_code
            }

    def get_current_organization(self, request, serialized=False):
        try:
            query_organization = Organization.objects.filter(id=request.headers["X-Organization-Key"]).first()

            if query_organization:
                if serialized:
                    return OrganizationSerializer(query_organization).data
                else:
                    return query_organization

            return False

        except Exception as e:
            return False

    def get_user_organization_access(self, request):
        try:
            user = self.authenticated_user(request)
            query_member = OrganizationMember.objects.filter(user=user).all()

            if query_member:
                return query_member
            else:
                return False

        except Exception as e:
            return False

    def get_current_team(self, request, serialized=False):
        try:
            query_team = Team.objects.filter(id=request.headers["X-Team-Key"]).first()

            if query_team:
                if serialized:
                    return TeamSerializer(query_team).data
                else:
                    return query_team

            return False

        except Exception as e:
            return False

    def get_user_team_access(self, request):
        try:
            user = self.authenticated_user(request)
            query_member = TeamMember.objects.filter(user=user).all()

            if query_member:
                return query_member
            else:
                return False

        except Exception as e:
            return False
