from django.urls import path
from . import views  
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SplitViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'expenses', SplitViewSet)

app_name = 'Split'

urlpatterns = [
    path('', include(router.urls)),
]