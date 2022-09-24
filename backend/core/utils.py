from core.models import Role, Team, TeamMembership, Topic


def get_role_id_by_role_name(role_name):
    try:
        role = Role.objects.get(name=role_name)
        return role.id
    except Exception as e:
        return None

def get_all_roles_available():
    roles = Role.objects.all()
    return roles

def is_team_instance_exists(team_id):
    return Team.objects.filter(id=team_id).exists()

def is_user_team_membership_exists(user_id, team_id):
    return TeamMembership.objects.filter(user_id=user_id, team_id=team_id).exists()

def has_admin_team_membership(user_id, team_id):
    return TeamMembership.objects.filter(user_id=user_id, team_id=team_id, role_id=get_role_id_by_role_name('admin')).exists()

def has_member_team_membership(user_id, team_id):
    return TeamMembership.objects.filter(user_id=user_id, team_id=team_id, role_id=get_role_id_by_role_name('member')).exists()

def has_team_membership(user_id, team_id):
    return TeamMembership.objects.filter(user_id=user_id, team_id=team_id).exists()

def get_team_id_by_topic_id(topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
        return topic.team_id
    except Exception as e:
        return None
