from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from utils.openai.openai_helper import OpenAIHelper
import logging


class UseView(APIView):
    permission_classes = [IsAuthenticated]
    user_helper = UserHelper()
    openai_helper = OpenAIHelper()

    def post(self, request):
        try:
            content = self.openai_helper.generate(
                request=request, prompt_id=request.data["id"],
                prompt_language=request.data["lang"], prompt_data=request.data["data"]
            )

        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True, "data": content}, status=status.HTTP_200_OK)
