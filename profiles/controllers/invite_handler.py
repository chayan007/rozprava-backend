from django.db.models import Q

from profiles.models import Profile, InviteLead


class InviteHandler:

    @staticmethod
    def check_and_process_invite_lead(profile_uuid: str):
        """
        Check if a profile was created on basis of a lead and mark it.

        If a newly registered profile was created using a mail/mobile registered in your
        invite leads, then the referrer user should be notified/gifted.
        """
        profile = Profile.objects.get(profile_uuid)
        assert profile is not None

        invite_lead = InviteLead.objects.filter(
            (Q(invited_type=InviteLead.InviteMedium.EMAIL) & Q(invited_contact=profile.user.email)) |
            (Q(invited_type=InviteLead.InviteMedium.MOBILE) & Q(invited_contact=profile.mobile_number))
        ).first()

        if invite_lead:
            invite_lead.has_registered = True
            invite_lead.save()
