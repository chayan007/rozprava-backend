from case.models import Case

from proof.controllers.core_proof_handler import CoreProofHandler
from proof.models import Proof


class CaseProofHandler(CoreProofHandler):

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

    def list(self):
        return self.case.proofs.all()
