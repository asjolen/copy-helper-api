from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user.models import Extended
from utils.user.user_helper import UserHelper
from user.serializers import ExtendedUserSerializer
import logging
import datetime


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    user_helper = UserHelper()

    def post(self, request):
        try:
            user = self.user_helper.authenticated_user(request)

            if "skipAuth0Fetch" in request.data and request.data["skipAuth0Fetch"] is True:
                # Manually insert user details
                extended_user, user = Extended.objects.update_or_create(
                    user=user, defaults={
                            "given_name": request.data["given_name"],
                            "family_name": request.data["family_name"],
                            "user_language": request.data["user_language"] if "user_language" in request.data["given_name"] else None,
                        }
                )
            else:
                create_extended_user = False

                extended_user_updated_at = Extended.objects.filter(
                    user=user, updated_at__lte=datetime.datetime.now()-datetime.timedelta(minutes=60)
                )

                extended_user_exists = Extended.objects.filter(user=user)

                # Update if X minutes passed or if user does not exist
                if extended_user_updated_at.exists():
                    create_extended_user = True
                elif not extended_user_exists.exists():
                    create_extended_user = True

                if create_extended_user:
                    fetched_user = self.user_helper.fetch_user(request)

                    if fetched_user["status"] != 200:
                        raise Exception(fetched_user["status"])

                    extended_user, user = Extended.objects.update_or_create(
                        user=user, defaults={
                            "email": fetched_user["result"]["email"] if "email" in fetched_user["result"] else None,
                            "given_name": fetched_user["result"]["given_name"] if "given_name" in fetched_user["result"] else None,
                            "family_name": fetched_user["result"]["family_name"] if "family_name" in fetched_user["result"] else None,
                            "name": fetched_user["result"]["name"] if "name" in fetched_user["result"] else None,
                            "user_language": fetched_user["result"]["user_language"] if "user_language" in fetched_user["user_language"] else None,
                            "picture": fetched_user["result"]["picture"] if "picture" in fetched_user["result"] else None,
                            "settings": {},

                            "email_verified": fetched_user["result"]["email_verified"] if "email_verified" in fetched_user["result"] else None,
                        }
                    )
                else:
                    extended_user = extended_user_exists.first()

            return Response({"status": True, "data": ExtendedUserSerializer(extended_user).data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            user = self.user_helper.authenticated_user(request)
            user_data = list()

            user_data.append({
                "id": user.id
            })

        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True, "data": user_data}, status=status.HTTP_200_OK)