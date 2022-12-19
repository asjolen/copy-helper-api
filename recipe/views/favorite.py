from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from utils.api.permissions import IsOrganizationAndTeamMember
from utils.openai.openai_helper import OpenAIHelper
from recipe.models import Favorites
from utils.firebase.firebase_helper import FirebaseHelper
from datetime import datetime
from django.db import transaction
import logging


class FavoriteView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAndTeamMember]
    user_helper = UserHelper()
    openai_helper = OpenAIHelper()
    firebase_helper = FirebaseHelper()

    def post(self, request):
        with transaction.atomic():
            try:
                user = self.user_helper.authenticated_user(request)
                team = self.user_helper.get_current_team(request)
                favorite = Favorites.objects.filter(user=user, team=team, recipe_id=request.data["recipe"])

                if favorite.exists():
                    favorite.delete()
                else:
                    Favorites.objects.create(user=user, team=team, recipe_id=request.data["recipe"])
            except Exception as e:
                transaction.set_rollback(True)
                logging.error(str(e))
                return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Commit transaction
        transaction.commit()

        self.firebase_helper.set(path=["user", str(team.id), "updated"], value=str(datetime.now()))
        return Response({"status": True}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            user = self.user_helper.authenticated_user(request)
            team = self.user_helper.get_current_team(request)
            favorites = Favorites.objects.filter(user=user, team=team).all()
            favorite_data = list()

            for favorite in favorites:
                favorite_data.append({
                    "id": favorite.recipe.id,
                    "identifier": favorite.recipe.identifier,
                    "data": favorite.recipe.data,
                    "settings": favorite.recipe.settings
                })

        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True, "data": favorite_data}, status=status.HTTP_200_OK)
