from debate.models import Debate

from proof.controllers.core_proof_handler import CoreProofHandler
from proof.models import Proof


class DebateProofHandler(CoreProofHandler):

    def __init__(self, debate_uuid: str):
        self.debate = Debate.records.get(uuid=debate_uuid)

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
                self.debate.proofs.add(*proofs)
                self.debate.save()
                return True
        except (AttributeError, ValueError, IndexError):
            return False

    def list(self):
        return self.debate.proofs.all()
