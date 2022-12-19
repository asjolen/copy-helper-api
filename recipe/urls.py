from django.urls import path
from recipe.views.recipe import RecipeView
from recipe.views.favorite import FavoriteView
from recipe.views.use import UseView

urlpatterns = [
    path('recipe/', RecipeView.as_view()),
    path('favorite/', FavoriteView.as_view()),
    path('use/', UseView.as_view())
]