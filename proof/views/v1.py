from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from proof.controllers.case_proof_handler import CaseProofHandler
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


class DebateProofView(GenericAPIView):

    def post(self, request, debate_uuid):
        """Upload proof for the debate."""
        is_uploaded = DebateProofHandler(
            debate_uuid
        ).add(
            request.user, request.FILES
        )
        if is_uploaded:
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': 'Proofs uploaded successfully for the debate.'}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'error': 'Proofs failed to upload for the debate.'}
        )

    def delete(self, request, *args, **kwargs):
        """Delete proof for the debate."""
        is_deleted = DebateProofHandler(
            kwargs.get('debate_uuid')
        ).delete(
            request.user, kwargs.get('proof_uuid')
        )
        if is_deleted:
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': 'Proofs deleted successfully for the debate.'}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'error': 'Proofs failed to upload for the debate.'}
        )


class CaseProofListView(ListAPIView):
    """List all proofs for a specific case."""

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


class CaseProofView(GenericAPIView):

    def post(self, request, case_slug):
        """Upload proof for the case."""
        is_uploaded = CaseProofHandler(case_slug).add(
            request.user, request.FILES
        )
        if is_uploaded:
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': 'Proofs uploaded successfully for the case.'}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'error': 'Proofs failed to upload for the case.'}
        )

    def delete(self, request, *args, **kwargs):
        """Delete proof for the case."""
        is_deleted = DebateProofHandler(
            kwargs.get('debate_uuid')
        ).delete(
            request.user, kwargs.get('proof_uuid')
        )
        if is_deleted:
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': 'Proofs deleted successfully for the case.'}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'error': 'Proofs failed to upload for the case.'}
        )

