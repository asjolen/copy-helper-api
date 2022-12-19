from django.urls import path
from object.views.management.object import ObjectView
from object.views.management.move import MoveObjectView
from object.views.management.favorite import FavoriteView
from object.views.management.reserve import ReserveView

urlpatterns = [
    path('object/', ObjectView.as_view()),
    path('move/', MoveObjectView.as_view()),
    path('favorite/', FavoriteView.as_view()),
    path('reserve/', ReserveView.as_view())
]
