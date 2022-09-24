from rest_framework import viewsets, mixins, authentication, permissions
from core.models import Topic
from core import custom_permissions
from .serializers import TopicSerializer
from .filters import TopicsByTeamIdFilter


class TopicViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """
    Team Viewset.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.TopicViewSetPermission
    ]
    serializer_class = TopicSerializer
    filter_backends = [TopicsByTeamIdFilter]
    search_fields = ['=team__id']
    queryset = Topic.objects.all()

