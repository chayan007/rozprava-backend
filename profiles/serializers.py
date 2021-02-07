from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import Profile


class UserSerializer(serializers.ModelSerializer):
    """Serialize user model object."""

    full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(obj: User):
        return obj.get_full_name()

    class Meta:

        model = User
        fields = (
            'username',
            'email',
            'username',
            'full_name'
        )


class ProfileSerializer(serializers.ModelSerializer):
    """Serialize profile model object."""

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = (
            'user',
            'dob',
            'display_pic',
            'mobile_number',
            'address',
            'country',
            'is_verified',
            'celebrity_rank',
            'is_celebrity',
            'profession',
            'relationship_status'
        )

