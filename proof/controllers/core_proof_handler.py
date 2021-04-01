from rest_framework.exceptions import ValidationError

from proof.models import Proof


class CoreProofHandler:

    @staticmethod
    def delete(user, proof_uuid: str):
        proof = Proof.objects.get(uuid=proof_uuid)
        if proof.profile == user.profile:
            proof.is_deleted = True
            proof.save()
            return True
        raise ValidationError('User does not have privilege to delete this proof.')

    @staticmethod
    def list():
        return Proof.records.all()
