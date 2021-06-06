from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.constants import PROFILE_PAGE_URL
from profiles.models import Group, Profile, FollowerMap
from profiles.utilities import check_if_request_authenticated


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
    profile_link = serializers.SerializerMethodField()
    authenticated_details = serializers.SerializerMethodField()

    @staticmethod
    def is_following(follower, following) -> bool:
        return FollowerMap.objects.filter(
            follower=follower,
            following=following
        ).exists()

    def get_authenticated_details(self, obj):
        """Return details that authenticated profiles can see."""
        request = self.context.get('request')
        if check_if_request_authenticated(request):
            return {}
        return {
            'is_following': self.is_following(request.user.profile, obj)
        }

    def get_profile_link(self, obj):
        """Generate profile link using the object."""
        return PROFILE_PAGE_URL.format(
            base_url=settings.BASE_URL,
            username=obj.user.username
        )

    class Meta:
        model = Profile
        fields = (
            'user',
            'dob',
            'bio',
            'display_pic',
            'mobile_number',
            'profile_link',
            'address',
            'country',
            'is_verified',
            'celebrity_rank',
            'is_celebrity',
            'profession',
            'relationship_status'
        )


class GroupSerializer(serializers.ModelSerializer):
    """Serialize Group model object."""

    admins = ProfileSerializer(read_only=True, many=True)
    profiles = ProfileSerializer(read_only=True, many=True)
    created_by = ProfileSerializer()

    class Meta:

        model = Group
        fields = (
            'name',
            'description',
            'profiles',
            'is_paid',
            'admins',
            'created_by',
            'interview',
            'privacy'
        )
