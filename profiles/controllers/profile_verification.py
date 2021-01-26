from base.exceptions import AlreadyExistsError

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
            raise AlreadyExistsError('Identity Document already exists and auditing pending.')
        identity_doc_obj = IdentityDocument.objects.create(
            profile=self.profile,
            id_number=id_number,
            identity_type=identity_type,
            image=image
        )
        # Invoke task to send mail to admins for validation
        return identity_doc_obj
