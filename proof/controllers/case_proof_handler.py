from sentry_sdk import capture_exception

from case.models import Case

from proof.controllers.core_proof_handler import CoreProofHandler
from proof.models import Proof


class CaseProofHandler(CoreProofHandler):

    def __init__(self, case_slug: str):
        self.case = Case.records.get(slug=case_slug)

    def add(self, user, files):
        proofs = []
        try:
            for x in range(1, 1 + 5):
                proof_file = files.get('proof_{}'.format(x))
                if proof_file:
                    proof = Proof.objects.create(**{
                        'profile': user.profile,
                        'file': proof_file
                    })
                    proofs.append(proof)
            if proofs:
                self.case.proofs.add(*proofs)
                self.case.save()
                return True
        except (AttributeError, ValueError, IndexError) as err:
            capture_exception(err)
            return False

    def list(self):
        return self.case.proofs.all()
