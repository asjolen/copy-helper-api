from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
import logging


class CustomView(APIView):
    permission_classes = [IsAuthenticated]
    user_helper = UserHelper()

    def post(self, request):
        try:
            pass

        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True}, status=status.HTTP_200_OK)
