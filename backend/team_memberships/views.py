from rest_framework import viewsets, mixins, authentication, permissions
from core.models import TeamMembership
from core import custom_permissions
from .serializers import TeamMembershipSerializer


class TeamMembershipViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    """
    TeamMembership Viewset.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.TeamMembershipViewSetPermission
    ]
    serializer_class = TeamMembershipSerializer
    queryset = TeamMembership.objects.all().order_by('joined_on')

