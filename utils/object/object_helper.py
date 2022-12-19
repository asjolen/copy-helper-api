from object.models import Object, Favorite, Access
from utils.user.user_helper import UserHelper
from object.serializers import AccessSerializer
from django.db.models import Q


class ObjectHelper:
    OBJECT_TYPE_COLLECTION = 1
    OBJECT_TYPE_ITEM = 10

    EDITABLE_BY_EDITORS = 1
    EDITABLE_BY_ACCESS = 10

    def has_access_to_object(self, request, user, obj):
        user_helper = UserHelper()

        access = Access.objects.filter(Q(team=user_helper.get_current_team(request)) | Q(user=user), object_id=obj.id)
        current_team_access = False

        if obj.team.id == user_helper.get_current_team(request).id:
            current_team_access = True

        if access.exists() or current_team_access:
            return True
        else:
            return False

    def retrieve_objects_data(self, user, objects):
        extra_info = list()
        for obj in objects:
            object_info = dict()
            object_info["id"] = obj.id

            # Append relevant information
            query_favorite = Favorite.objects.filter(object=obj.id, user=user)
            object_info["favorite"] = True if query_favorite.exists() else False

            # Access
            access_data = Access.objects.filter(object=obj.id).all()
            object_info["access"] = list()

            for access in access_data:
                object_info["access"].append(AccessSerializer(access).data)

            if obj.type == self.OBJECT_TYPE_COLLECTION:
                child_count = list()
                for child in Object.objects.filter(id=obj.id).first().get_descendants(include_self=False):
                    if not child.deleted:
                        child_count.append(child)

                object_info["children_count"] = len(child_count)

            extra_info.append(object_info)
        return dict({
            "objects": objects,
            "extra": extra_info
        })
