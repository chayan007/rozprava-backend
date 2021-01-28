from base.exceptions import AlreadyExistsError

from profiles.models import Profile, IdentityDocument


class ProfileVerification:

    @staticmethod
    def get_identity_document(identity_document_uuid: str):
        return IdentityDocument.objects.get(uuid=identity_document_uuid)

    @staticmethod
    def request(profile: Profile, celebrity_rank: int, identity_type: str, id_number: str, image):
        """Place request for profile verification."""
        profile.celebrity_rank = celebrity_rank
        profile.save()

        existing_document = IdentityDocument.objects.filter(
            profile=profile,
            id_number=id_number,
            identity_type=identity_type,
            is_audited=False
        )
        if existing_document:
            raise AlreadyExistsError('Identity Document already exists and auditing pending.')

        identity_doc_obj = IdentityDocument.objects.create(
            profile=profile,
            id_number=id_number,
            identity_type=identity_type,
            image=image
        )
        # Invoke task to send mail to admins for validation
        return identity_doc_obj

    def approve(self, identity_document_uuid: str, celebrity_rank: int = None):
        """Approve the profile verification flow."""
        # Step 1: Mark the identity document as valid.
        identity_document_obj = self.get_identity_document(identity_document_uuid)
        identity_document_obj.is_valid = True
        identity_document_obj.is_audited = True
        identity_document_obj.save()

        # Step 2: Mark the profile as celebrity with appropriate celebrity status.
        profile = identity_document_obj.profile
        profile.is_verified = True
        profile.is_celebrity = True
        profile.celebrity_rank = celebrity_rank or profile.celebrity_rank
        profile.save()

    def reject(self, identity_document_uuid: str):
        """Reject the profile verification flow."""
        identity_document_obj = self.get_identity_document(identity_document_uuid)
        identity_document_obj.is_valid = False
        identity_document_obj.is_audited = True
        identity_document_obj.save()
