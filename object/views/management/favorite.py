from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from utils.api.permissions import IsOrganizationAndTeamMember
from object.models import Object, Favorite
from utils.firebase.firebase_helper import FirebaseHelper
from datetime import datetime
from django.db import transaction
from utils.object.object_helper import ObjectHelper
from utils.api.responses import APIResponses
import logging


class FavoriteView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAndTeamMember]
    user_helper = UserHelper()
    firebase_helper = FirebaseHelper()
    object_helper = ObjectHelper()

    def post(self, request):
        with transaction.atomic():
            try:
                user = self.user_helper.authenticated_user(request)
                team = self.user_helper.get_current_team(request, serialized=False)
                query_object = Object.objects.filter(team=team, id=request.data["id"]).first()

                if not self.object_helper.has_access_to_object(request, user, query_object):
                    raise Exception(APIResponses.ERROR_INVALID_ACCESS)

                query_favorite = Favorite.objects.filter(object=query_object, user=user)

                if query_favorite.exists():
                    query_favorite.delete()
                else:
                    Favorite.objects.create(object=query_object, user=user)
            except Exception as e:
                transaction.set_rollback(True)
                logging.error(str(e))
                return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Commit
        transaction.commit()

        # Notify firebase
        self.firebase_helper.set(path=["team", str(team.id), "objects", "updated"], value=str(datetime.now()))
        return Response({"status": True}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            user = self.user_helper.authenticated_user(request)
            return Response({"status": True}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)