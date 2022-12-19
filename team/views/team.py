from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from team.models import Team, Member as TeamMember
from utils.api.responses import APIResponses
import logging


class TeamView(APIView):
    permission_classes = [IsAuthenticated]
    user_helper = UserHelper()

    def get(self, request):
        try:
            user = self.user_helper.authenticated_user(request)
            membership = TeamMember.objects.filter(user=user.id).all()
            teams = list()

            for member in membership:
                teams.append({
                    "id": member.team.id,
                    "name": member.team.name,
                    "role": member.role,
                })
        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True, "data": teams}, status=status.HTTP_200_OK)

    def post(self, request):
        with transaction.atomic():
            try:
                user = self.user_helper.authenticated_user(request)
                organization = self.user_helper.get_current_organization(request)

                if "id" in request.data:
                    team = Team.objects.filter(id=request.data["id"]).first()
                    member = TeamMember.objects.filter(team=team, user=user, role=self.user_helper.TEAM_MANAGER)

                    if not member:
                        raise Exception(APIResponses.ERROR_INVALID_ACCESS)

                    # Check existing name
                    team_existing = Team.objects.filter(organization=organization, name=request.data["name"])
                    if team_existing.exists():
                        raise Exception(APIResponses.ERROR_NAME_TAKEN)

                    if "name" in request.data:
                        team.name = request.data["name"]

                    team.save()

                else:
                    # Check existing name
                    team_existing = Team.objects.filter(organization=organization, name=request.data["name"])
                    if team_existing.exists():
                        raise Exception(APIResponses.ERROR_NAME_TAKEN)

                    team = Team.objects.create(organization=organization, name=request.data["name"])
                    TeamMember.objects.create(team=team, user=user, role=self.user_helper.TEAM_MANAGER)

            except Exception as e:
                transaction.set_rollback(True)
                logging.error(str(e))
                return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        transaction.commit()
        return Response({"status": True}, status=status.HTTP_200_OK)
