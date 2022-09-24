from rest_framework import viewsets, mixins, authentication, permissions
from core.models import Team
from core import custom_permissions
from .serializers import TeamSerializer
from .filters import TeamOwnerFilter


class TeamViewSet(viewsets.ModelViewSet):
    """
    Team Viewset.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsTeamOwnerOrReadOnly
    ]
    serializer_class = TeamSerializer
    filter_backends = [TeamOwnerFilter]
    search_fields = ['=owner__id']
    queryset = Team.objects.all().order_by('created_on')

