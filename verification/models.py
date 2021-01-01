from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel
from profiles.models import Profile


class OTPVerification(BaseModel):
    """OTP Verification stack trace."""

    class VerifierTag(models.IntegerChoices):
        """Reason for generating OTP."""
        MAIL_VERIFICATION = 1, _('MAIL VERIFICATION')
        PHONE_VERIFICATION = 2, _('PHONE VERIFICATION')
        PASSWORD_RESET = 3, _('PASSWORD RESET')
        OTHER = 0, _('OTHER')

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    verifier_tag = models.IntegerField(choices=VerifierTag.choices)
    is_verified = models.BooleanField(default=False)
    additional_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(
            self.get_verifier_tag_display(),
            self.profile.user.get_full_name()
        )
