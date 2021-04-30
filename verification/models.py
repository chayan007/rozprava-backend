from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel

from notification.models import Notification

from profiles.models import Profile
from profiles.utilities import get_profile_verification_image_upload_path


class OTPVerification(BaseModel):
    """OTP Verification stack trace."""

    class VerifierTag(models.IntegerChoices):
        """Reason for generating OTP."""
        OTHER = 0, _('OTHER')
        MAIL_VERIFICATION = 1, _('MAIL VERIFICATION')
        PHONE_VERIFICATION = 2, _('PHONE VERIFICATION')
        PASSWORD_RESET = 3, _('PASSWORD RESET')

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    verifier_tag = models.IntegerField(choices=VerifierTag.choices)
    is_verified = models.BooleanField(default=False)
    notification_type = models.SmallIntegerField(choices=Notification.NotificationType.choices, default=Notification.NotificationType.EMAIL.value)
    additional_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(
            self.get_verifier_tag_display(),
            self.profile.user.get_full_name()
        )


class KYCVerification(BaseModel):

    class IdentityChoices(models.TextChoices):

        UIDAI = 'UIDAI'
        PAN = 'PAN'
        PASSPORT = 'PASSPORT'
        DRIVING_LICENSE = 'DRIVING_LICENSE'
        VOTER_ID = 'VOTER_ID'
        OTHER = 'OTHER'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    identity_type = models.CharField(max_length=20, choices=IdentityChoices.choices, default=IdentityChoices.OTHER.value)
    image = models.ImageField(upload_to=get_profile_verification_image_upload_path)
    id_number = models.CharField(max_length=100, null=True, blank=True)
    kyc_json = models.JSONField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)
    is_audited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.profile.user.get_full_name()}'
