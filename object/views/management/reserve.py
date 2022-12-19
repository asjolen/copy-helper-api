from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from utils.api.permissions import IsOrganizationAndTeamMember
from object.models import Reserved
from django.db import transaction
import logging


class ReserveView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAndTeamMember]
    user_helper = UserHelper()

    def post(self, request):
        with transaction.atomic():
            try:
                user = self.user_helper.authenticated_user(request)
                Reserved.objects.create(uuid=request.data["uuid"], user=user)

            except Exception as e:
                transaction.set_rollback(True)
                logging.error(str(e))
                return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True}, status=status.HTTP_200_OK)
