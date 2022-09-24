from rest_framework import viewsets, mixins, permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import (
    AuthTokenSerializer,
    UserCreateSerializer,
    UserListUpdateDestroySerializer
)
from django.contrib.auth import get_user_model

# Create your views here.

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserCreateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    A viewset for registering user.
    """
    serializer_class = UserCreateSerializer
    queryset = get_user_model().objects.all()


class UserListUpdateDestroyViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """
    A viewset for viewing, editing & deleting user intances for
    staff only.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserListUpdateDestroySerializer
    queryset = get_user_model().objects.all()

    # viewset methods available to override default set values.
    def get_queryset(self):
        return self.queryset.order_by('id')


class ProfileViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    """
    A viewset for viewing, editing authenticated self user profile.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListUpdateDestroySerializer
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)
