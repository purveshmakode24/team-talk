from rest_framework import serializers
from core.models import Comment, Topic



class CommentSerializer(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all()
    )
    team_id = serializers.UUIDField(
        source='topic.team.id',
        read_only=True
    )
    commented_by = serializers.CharField(
        source='commented_by.email',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'body', 'topic_id', 'team_id', 'commented_by', 'created_on']
        extra_kwargs = {'created_on': {'read_only': True}}

        def validate(self, attrs):
            request = self.context.get('request')

            topic = attrs.pop('topic_id')

            ## validating if requested current loggedin user is a team member in which he is commenting.
            ## Taking care of this (below part) in permissions.

            # if not has_team_membership(request.user.id, topic.team.id):
            #     msg = {'field_errors': ['You can not comment to this topic.']}
            #     raise serializers.ValidationError(msg)

            attrs['commented_by_id'] = request.user.id
            attrs['topic_id'] = topic.id

            return super().validate(attrs)