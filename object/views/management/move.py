from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from utils.api.permissions import IsOrganizationAndTeamMember
from object.models import Object
from utils.object.object_helper import ObjectHelper
from utils.tree.tree_helper import TreeHelper
from utils.firebase.firebase_helper import FirebaseHelper
from datetime import datetime
from django.db import transaction
import logging


class MoveObjectView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAndTeamMember]
    user_helper = UserHelper()
    object_helper = ObjectHelper()
    firebase_helper = FirebaseHelper()
    tree_helper = TreeHelper()

    def post(self, request):
        with transaction.atomic():
            try:
                team = self.user_helper.get_current_team(request, serialized=False)
                query_object = Object.objects.filter(team=team, id=request.data["move_object"]).first()

                if "move_to" in request.data and request.data["move_to"] != "root":
                    query_move_to = Object.objects.filter(team=team, id=request.data["move_to"]).first()
                    if query_move_to.type == self.object_helper.OBJECT_TYPE_COLLECTION:
                        query_object.move_to(query_move_to)
                else:
                    query_object.parent = None
                    query_object.save()
            except Exception as e:
                transaction.set_rollback(True)
                logging.error(str(e))
                return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Commit transaction
        transaction.commit()

        self.firebase_helper.set(path=["team", str(team.id), "objects", "updated"], value=str(datetime.now()))
        return Response({"status": True}, status=status.HTTP_200_OK)