from activity.models import Activity

from case.models import Case

from debate.models import Debate


class ReviewHandler:
    """Handle entire review based operations."""

    PERMISSIBLE_REPORTS_LIMIT = 10

    def put_case_for_review(self, case_uuid: str):
        """Check if case qualifies for review and trigger it."""
        case = Case.objects.get(uuid=case_uuid)
        reports = Activity.objects.filter(content_object=case, activity_type=Activity.ActivityChoices.REPORT.value)
        if len(reports) > self.PERMISSIBLE_REPORTS_LIMIT:
            case.status = Case.CaseStatus.UNDER_REVIEW.value
            case.save()

    def put_debate_for_review(self, debate_uuid: str):
        """Check if debate qualifies for review and trigger it."""
        debate = Debate.objects.get(uuid=debate_uuid)
        reports = Activity.objects.filter(content_object=debate, activity_type=Activity.ActivityChoices.REPORT.value)
        if len(reports) > self.PERMISSIBLE_REPORTS_LIMIT:
            debate.status = Debate.DebateStatus.UNDER_REVIEW.value
            debate.save()
