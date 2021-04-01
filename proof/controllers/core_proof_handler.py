from proof.models import Proof


class CoreProofHandler:

    @staticmethod
    def delete(proof_uuid):
        proof = Proof.objects.get(uuid=proof_uuid)
        proof.is_deleted = True
        proof.save()

    @staticmethod
    def list():
        return Proof.records.all()
