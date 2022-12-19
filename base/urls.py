"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from base.views import not_found, app_error

handler404 = not_found
handler500 = app_error

urlpatterns = [
    path('user/', include('user.urls')),
    path('object/', include('object.urls')),
    path('organization/', include('organization.urls')),
    path('team/', include('team.urls')),
    path('recipe/', include('recipe.urls')),
    path('subscription/', include('subscription.urls')),
]