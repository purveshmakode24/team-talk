from email import message
from rest_framework import permissions

from .utils import (
    get_team_id_by_topic_id,
    has_admin_team_membership,
    has_team_membership
)


class IsTeamOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow Team object access methods (PUT, DELETE, GET) only if it's a team owner,
    Else allow only (GET) methods.
    """
    message = {
        'errors': [
            'You are not the owner of Team and do not have permission to perform this action.'
        ]
    }
    # To check specifically retrive (get), update (put, patch) and destroy (delete).
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class TeamMembershipViewSetPermission(permissions.BasePermission):
    """
    list, retrive, update, partial update - membership: Staff
    create - membership: Current auth user or Staff
    destroy - membership: Self auth user
    """

    def has_permission(self, request, view):
        if view.action == 'list':
            return bool(request.user and request.user.is_staff)
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            # NEED TO ERIFY THIS PART AS THERE WILL BE MEMBERSHIP ID AND
            # NOT USER ID OR TEAM ID TO DELETE THIS INSTANCE.
            return obj.user_id == request.user.id
        return bool(request.user and request.user.is_staff)


class TopicViewSetPermission(permissions.BasePermission):
    """
    Only members can view the topics from that Team.
    Only Admin member can perform ('create', 'update', 'partial_update', 'destroy')
    """
    message = {
        "errors": "You do not have persmission to perform this action."
    }

    def has_permission(self, request, view):
        if view.action == 'list':
            self.message['errors'] = 'You are not a team member and do not have permission to view this content.'
            team_id = request.query_params.get('team_id')
            return bool(
                (request.user or request.user.is_staff) and
                has_team_membership(request.user.id, team_id)
            )
        elif view.action in ('create', 'update', 'partial_update', 'destroy'):
            self.message['errors'] = 'You are not a admin member of a team and do not have permission to do this action.'
            team_id = request.data.get('team_id')
            ## NEED TO VERIFY DESTROY (team_id)
            return bool(
                (request.user or request.user.is_staff) and
                has_admin_team_membership(request.user.id, team_id)
            )
        return False


class CommentViewSetPermission(permissions.BasePermission):
    """
    list - comments: All team members
    create - comments: All team members
    retrive - comments: Admin (staff) only
    update - comments: All team members own comments only
    destroy - comments: members own comments, Admin can delete any user/self comments.
    """

    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if view.action == 'list':
            self.message['errors'] = 'You are not a team member and do not have permission to view this content.'
            topic_id = request.query_params.get('topic_id')
            team_id = get_team_id_by_topic_id(topic_id)
            return bool(
                (request.user or request.user.is_staff) and
                has_team_membership(request.user.id, team_id)
            )
        elif view.action == 'create':
            self.message['errors'] = 'You are not a team member and do not have permission to perform this action.'
            topic_id = request.data.get('topic_id')
            team_id = get_team_id_by_topic_id(topic_id)
            return bool(
                (request.user or request.user.is_staff) and
                has_team_membership(request.user.id, team_id)
            )
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ('update', 'partial_update'):
            self.message['errors'] = 'You are not a owner of a comment and do not have permission to do this action.'
            topic_id = request.data.get('topic_id')
            team_id = get_team_id_by_topic_id(topic_id)
            return bool(
                (request.user or request.user.is_staff) and
                has_team_membership(request.user.id, team_id) and
                obj.commented_by_id == request.user.id
            )
        elif view.action == 'destroy':
            ## NEED TO VERIFY THIS PART FOR obj.topic.team.id
            return bool(
                (request.user or request.user.is_staff) and
                has_team_membership(request.user.id, obj.topic.team.id) and
                (obj.commented_by_id == request.user.id or
                has_admin_team_membership(request.user.id, obj.topic.team.id))
            )
        return False


