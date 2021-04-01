from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from proof.controllers.debate_proof_handler import DebateProofHandler
from proof.models import Proof
from proof.serializers import ProofSerializer


class DebateProofListView(ListAPIView):
    """List all proofs for a specific debate."""

    serializer_class = ProofSerializer
    model = Proof
    paginate_by = 10

    def get_queryset(self):
        debate_uuid = self.kwargs.get('debate_uuid')
        queryset = (
            DebateProofHandler(debate_uuid).list()
            if debate_uuid
            else self.model.records.all()
        )
        return queryset.order_by('-created_at')


class CaseProofListView(ListAPIView):
    """List all proofs for a specific debate."""

    serializer_class = ProofSerializer
    model = Proof
    paginate_by = 10

    def get_queryset(self):
        case_slug = self.kwargs.get('case_slug')
        queryset = (
            DebateProofHandler(case_slug).list()
            if case_slug
            else self.model.records.all()
        )
        return queryset.order_by('-created_at')

