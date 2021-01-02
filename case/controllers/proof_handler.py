from case.models import Case
from proof.models import Proof


class ProofHandler:

    def __init__(self, case_slug: str):
        self.case = Case.objects.get(slug=case_slug)

    def add(self, user, **kwargs):
        proofs = []
        for x in range(1, 1 + 5):
            proof_file = kwargs.get('proof_{}'.format(x), None)
            if proof_file:
                proof = Proof.objects.create(**{
                    'profile': user.profile,
                    'file': proof_file
                })
                proofs.append(proof)
        if proofs:
            self.case.proofs.add(*proofs)
            self.case.save()

    @staticmethod
    def delete(proof_uuid):
        proof = Proof.objects.get(uuid=proof_uuid)
        proof.delete()

    def list(self):
        return self.case.proofs.all()
