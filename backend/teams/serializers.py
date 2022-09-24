from rest_framework import serializers
from core.models import Team, TeamMembership


class TeamSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(
        source='owner.email',
        read_only=True
    )
    membership_status = serializers.SerializerMethodField()


    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'owner', 'created_on', 'membership_status']
        extra_kwargs = {'created_on': {'read_only': True}}
        # depth=1

    def validate(self, attrs):
            request = self.context.get('request')
            attrs['owner_id'] = request.user.id

            return super().validate(attrs)

    def get_membership_status(self, obj):
        request = self.context['request']
        membership_status = 'not_joined'

        membership = TeamMembership.objects.filter(
            team_id=obj.id,
            user=request.user
        )

        if membership.exists():
            membership_status =  {
                'status':'create',
                'membership_id': membership[0].id
            } if membership[0].role.name == 'admin' else {
                'status': 'joined',
                'membership_id': membership[0].id
            }

        return membership_status

    def create(self, validated_data):
        return Team.objects.create_team(**validated_data)