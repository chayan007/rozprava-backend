from proof.models import Proof


class CoreProofHandler:

    @staticmethod
    def delete(proof_uuid):
        proof = Proof.objects.get(uuid=proof_uuid)
        proof.delete()

    @staticmethod
    def list():
        return Proof.objects.all()
