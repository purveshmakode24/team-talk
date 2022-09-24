from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from teams.serializers import TeamSerializer
from django.utils.translation import gettext_lazy as _


class UserListUpdateDestroySerializer(serializers.ModelSerializer):
    teams_created = TeamSerializer(source='teams', many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'teams_created']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserCreateSerializer(UserListUpdateDestroySerializer):
    class Meta(UserListUpdateDestroySerializer.Meta):
        fields = UserListUpdateDestroySerializer.Meta.fields + ['password']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validate_data):
            return get_user_model().objects.create_user(**validate_data)


# Simple serializier that isn't linked to a model
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    # validate method for auth token serializer.
    # validate method is called at validation stage by a view.
    # When a data/attrs/payload is posted to the view it's going to pass-
    # it to the serializer and it's going to call the validate-
    # to validate if the data is correct.
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Incorrect email or password.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
