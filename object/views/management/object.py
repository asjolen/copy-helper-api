from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utils.user.user_helper import UserHelper
from utils.api.permissions import IsOrganizationAndTeamMember
from object.models import Object, Access, Editor
from utils.object.object_helper import ObjectHelper
from utils.tree.tree_helper import TreeHelper
from utils.firebase.firebase_helper import FirebaseHelper
from datetime import datetime
from django.db import transaction
from django.db.models import Q
from itertools import chain
import logging


class ObjectView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAndTeamMember]
    user_helper = UserHelper()
    object_helper = ObjectHelper()
    firebase_helper = FirebaseHelper()
    tree_helper = TreeHelper()

    def post(self, request):
        with transaction.atomic():
            try:
                user = self.user_helper.authenticated_user(request)
                team = self.user_helper.get_current_team(request, serialized=False)
                object_id = request.data["id"] if "id" in request.data else None

                obj, obj_created = Object.objects.update_or_create(id=object_id, team=team, defaults={
                    "name": request.data["name"],
                    "type": request.data["type"],
                    "settings": request.data["settings"],
                })

                obj.save()

                # #######################################
                # Editors
                # #######################################
                Editor.objects.update_or_create(object=obj, user=user)

                # Save in collection
                if "parent" in request.data:
                    obj = Object.objects.filter(id=obj.id, team=team).first()

                    if request.data["parent"] != "None" and request.data["parent"] is not None:
                        parent = Object.objects.filter(team=team, id=request.data["parent"]).first()
                        obj.parent = parent
                    else:
                        obj.parent = None

                    obj.save()
            except Exception as e:
                transaction.set_rollback(True)
                logging.error(str(e))
                return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Commit transaction
        transaction.commit()

        self.firebase_helper.set(path=[
            "team", str(team.id), "objects", "updated"
        ], value=str(datetime.now()))

        return Response({"status": True, "data": {"id": obj.id}}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            user = self.user_helper.authenticated_user(request)
            team = self.user_helper.get_current_team(request, serialized=False)

            if "type" in request.GET:
                types = [request.GET["type"]]

                if "," in request.GET["type"]:
                    types = request.GET["type"].split(",")

                objects = Object.objects.filter(team=team, type__in=types, deleted__isnull=True).all()
            elif "deleted" in request.GET:
                objects = Object.objects.filter(team=team, deleted__isnull=False).all()
            elif "id" in request.GET:
                objects = Object.objects.filter(team=team, id=request.GET["id"]).all()
            else:
                objects = Object.objects.filter(team=team, deleted__isnull=True).all()

            # #################################################
            # Get shared access objects
            # #################################################
            access_objects_list = Access.objects.filter(
                Q(team=team) | Q(user=user)
            ).exclude(object_id__in=objects.values_list("id")).values_list("object_id")

            access_objects = Object.objects.filter(
                id__in=access_objects_list, deleted__isnull=True,
            ).all()

            objects = list(chain(objects, access_objects))

            # #################################################
            # Append information
            # #################################################
            return_objects = None
            return_extra_data = None
            data = self.object_helper.retrieve_objects_data(user, objects)
            if data:
                return_extra_data = data["extra"]
                return_objects = data["objects"]
                return_objects = self.tree_helper.create_tree_list(return_objects, [
                    "id", "name", "type", "created_at", "updated_at", "parent", "settings", "team"
                ])

            return Response({"status": True, "data": return_objects, "extra": return_extra_data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        with transaction.atomic():
            try:
                team = self.user_helper.get_current_team(request, serialized=False)
                query_object = Object.objects.filter(id=request.GET["id"], team=team).first()

                for child in query_object.get_descendants(include_self=True):
                    child.deleted = datetime.now()
                    child.save()
            except Exception as e:
                transaction.set_rollback(True)
                logging.error(str(e))
                return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Commit transaction
        transaction.commit()

        self.firebase_helper.set(path=[
            "team", str(team.id), "objects", "updated"
        ], value=str(datetime.now()))

        return Response({"status": True}, status=status.HTTP_200_OK)
