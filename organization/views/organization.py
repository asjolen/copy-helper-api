from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from organization.models import Organization, Member as OrganizationMember
from utils.api.responses import APIResponses
import logging


class OrganizationView(APIView):
    permission_classes = [IsAuthenticated]
    user_helper = UserHelper()

    def post(self, request):
        with transaction.atomic():
            try:
                user = self.user_helper.authenticated_user(request)
                if "id" in request.data:
                    organization = Organization.objects.filter(id=request.data["id"]).first()
                    member = OrganizationMember.objects.filter(
                        organization=organization, user=user, role=self.user_helper.ORGANIZATION_MANAGER
                    ).first()

                    if not member:
                        raise Exception(APIResponses.ERROR_INVALID_ACCESS)

                    if "name" in request.data:
                        organization.name = request.data["name"]
                    if "website" in request.data:
                        organization.website = request.data["website"]

                    organization.save()

                else:
                    organization = Organization.objects.create(
                        name=request.data["name"], website=request.data["website"]
                    )

                    OrganizationMember.objects.create(
                        organization=organization, user=user, role=self.user_helper.ORGANIZATION_MANAGER
                    )

            except Exception as e:
                transaction.set_rollback(True)
                logging.error(str(e))
                return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        transaction.commit()
        return Response({"status": True}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            user = self.user_helper.authenticated_user(request)
            query_membership = OrganizationMember.objects.filter(user=user.id).all()
            organization = list()

            for member in query_membership:
                organization.append({
                    "id": member.organization.id,
                    "name": member.organization.name,
                    "role": member.role,
                })
        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True, "data": organization}, status=status.HTTP_200_OK)
