from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from recipe.models import Recipes, Favorites
from utils.api.permissions import IsOrganizationAndTeamMember
import logging


class RecipeView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAndTeamMember]
    user_helper = UserHelper()

    def get(self, request):
        try:
            user = self.user_helper.authenticated_user(request)
            team = self.user_helper.get_current_team(request)

            recipes = Recipes.objects.all()
            favorites = Favorites.objects.filter(user=user, team=team)
            data = list()
            favorites_data = list()

            for recipe in recipes:
                data.append({
                    "id": recipe.id,
                    "identifier": recipe.identifier,
                    "data": recipe.data,
                    "fields": recipe.fields,
                    "settings": recipe.settings
                })

            for favorite in favorites:
                favorites_data.append({
                    "recipe": favorite.recipe.id
                })

        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True, "data": data, "favorites": favorites_data}, status=status.HTTP_200_OK)

