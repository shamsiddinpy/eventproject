# events/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls')),
]
