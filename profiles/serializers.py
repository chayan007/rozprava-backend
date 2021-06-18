from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_auth.models import TokenModel
from rest_auth.serializers import UserDetailsSerializer
from rest_auth.utils import import_callable
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
            'relationship_status',
            'authenticated_details'
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


class RegisterSerializer(serializers.Serializer):
    """Wrapper serializer over all-auth serializer."""

    username = serializers.CharField(
        max_length=1,
        min_length=50,
        required=True
    )
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)

    @staticmethod
    def validate_username(username: str):
        return get_adapter().clean_username(username)

    @staticmethod
    def validate_email(email: str):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(_("A user is already registered with this e-mail address."))
        return email

    @staticmethod
    def validate_password1(password: str):
        return get_adapter().clean_password(password)

    def validate(self, data: dict):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user: User):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        user.profile.mobile_number = self.cleaned_data.get('mobile_number')
        user.profile.save()

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name'),
            'last_name': self.validated_data.get('last_name'),
            'mobile_number': self.validated_data.get('mobile_number')
        }

    def save(self, request):
        adapter = get_adapter()

        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)

        self.custom_signup(request, user)
        setup_user_email(request, user, [])

        return user


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        profile = obj['user'].profile
        user_data = ProfileSerializer(profile, context=self.context).data
        return user_data
