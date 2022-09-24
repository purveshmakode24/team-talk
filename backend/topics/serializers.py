from rest_framework import serializers
from core.models import Topic, Team


class TopicSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(
        source='creator.email',
        read_only=True
    )
    team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())


    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'creator', 'team_id']

    def validate(self, attrs):
            request = self.context.get('request')
            team=attrs.pop('team_id')

            # VALIDATING request.user.id in PERMISSIONS
            # to check if requested user is a owner of a topic/team.
            attrs['creator_id'] = request.user.id
            attrs['team_id'] = team.id

            return super().validate(attrs)
