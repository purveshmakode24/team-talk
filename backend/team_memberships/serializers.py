from rest_framework import serializers
from core.utils import get_role_id_by_role_name, is_user_team_membership_exists
from core.models import TeamMembership, Team



class TeamMembershipSerializer(serializers.ModelSerializer):
    # Custom fk value instad of fk/pk integer.
    role = serializers.CharField(
        source='role.name',
        read_only=True
    )
    # Custom attr name for fk (read only).
    user_id = serializers.UUIDField(read_only=True)
    # Custom attr name for fk (write and read).
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all()
    )

    class Meta:
        model = TeamMembership
        fields = ['id', 'role', 'user_id', 'team_id', 'joined_on']
        extra_kwargs = {'joined_on': {'read_only': True}}

        def validate(self, attrs):
            request = self.context.get('request')

            team = attrs.pop('team_id')

            attrs['team_id'] = team.id
            # curent auth user should noy already a member of the requested team.
            attrs['user_id'] = request.user.id
            attrs['role_id'] = get_role_id_by_role_name('member')

            # User below validation or User UniqueTogetherValidator for custom fields from serializers.
            if is_user_team_membership_exists(attrs['user_id'], attrs['team_id']):
                msg = {'errors': ['User is already a member of the team.']}
                raise serializers.ValidationError(msg)

            return super().validate(attrs)