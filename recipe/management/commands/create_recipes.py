from django.core.management.base import BaseCommand, CommandError
from utils.firebase.firebase_helper import FirebaseHelper
from recipe.models import Recipes
import os
import json


class Command(BaseCommand):
    help = 'Create recipes'
    firebase_helper = FirebaseHelper()

    def handle(self, *args, **options):
        module_dir = os.path.dirname(__file__)  # get current directory
        json_file = json.load(open(os.path.join(module_dir, 'recipes.json'), 'r'))

        for data in json_file["data"]:
            print("Adding recipe", data["identifier"])
            Recipes.objects.update_or_create(
                identifier=data["identifier"], defaults={
                    "data": data["data"],
                    "fields": data["fields"],
                    "settings": data["settings"]
                }
            )
