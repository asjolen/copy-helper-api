from mptt.templatetags.mptt_tags import cache_tree_children
from django.core import serializers
import json


class TreeHelper:
    def create_tree_list(self, objects, keys):
        tree = cache_tree_children(objects)
        returnable = list()

        for item in tree:
            returnable.append(self.recursive_node_to_dict(item, keys))

        return returnable

    def recursive_node_to_dict(self, node, keys):
        result = {}

        for key in keys:
            serialized = json.loads(serializers.serialize("json", [node]))[0]
            if key == "id":
                result[key] = serialized["pk"]
            else:
                result[key] = serialized["fields"][key]

        children = [self.recursive_node_to_dict(c, keys) for c in node.get_children()]

        if children:
            result['children'] = children

        return result

class ObjectNotationFix(object):
    def __getitem__(self, arg):
        return arg
