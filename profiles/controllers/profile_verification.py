from profiles.models import Profile, IdentityDocument


class ProfileVerification:

    def __init__(self, profile: Profile):
        self.profile = profile

    def request(self, identity_type: str, id_number: str, image):
        """Place request for profile verification."""
        existing_document = IdentityDocument.objects.filter(
            profile=self.profile,
            id_number=id_number,
            identity_type=identity_type,
            is_audited=False
        )
        if existing_document:
            raise