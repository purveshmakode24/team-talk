from rest_framework import viewsets, mixins, authentication, permissions
from core.models import Comment
from core import custom_permissions
from .serializers import CommentSerializer
from .filters import CommentsByTopicIdFilter


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """
    Comment Viewset.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.CommentViewSetPermission
    ]
    serializer_class = CommentSerializer
    filter_backends = [CommentsByTopicIdFilter]
    search_fields = ['=topic__id']
    queryset = Comment.objects.all().order_by('created_on')

