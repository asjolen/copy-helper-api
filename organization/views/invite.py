from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from utils.api.permissions import IsOrganizationManager
from organization.models import Organization, Member as OrganizationMember, Invitation
from utils.api.responses import APIResponses
import logging


class InviteView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationManager]
    user_helper = UserHelper()

    def post(self, request):
        with transaction.atomic():
            try:
                user = self.user_helper.authenticated_user(request)
                organization = self.user_helper.get_current_organization(request)
                email = request.data["email"] if "email" in request.data else None
                role = request.data["role"] if "role" in request.data else self.user_helper.ORGANIZATION_MEMBER

                check_existing = Invitation.objects.filter(email=email, organization=organization).exists()

                if check_existing:
                    raise Exception(APIResponses.ERROR_NAME_TAKEN)

                Invitation.objects.create(
                    email=email,
                    role=role,
                    organization=organization,
                    invited_by=user
                )

            except Exception as e:
                transaction.set_rollback(True)
                logging.error(str(e))
                return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        transaction.commit()
        return Response({"status": True}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            organization = self.user_helper.get_current_organization(request)
            data = list()

            invitations = Invitation.objects.filter(organization=organization).all()

            for invitation in invitations:
                data.append({
                    "email": invitation.email,
                    "role": invitation.role
                })

        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True, "data": data}, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            organization = self.user_helper.get_current_organization(request)
            invitation_id = request.data["id"] if "id" in request.data else None

            Invitation.objects.filter(id=invitation_id, organization=organization).delete()

        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True}, status=status.HTTP_200_OK)
