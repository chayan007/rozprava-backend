from activity.models import Activity

from case.models import Case


def get_case_metrics(case: Case):
    """Get case activity metrics."""
    try:
        return {
            Activity.objects.filter(content_type__model='case', activity_type=Activity.ActivityChoices.REPORT, object_id=case.uuid).count(),
            Activity.objects.filter(content_type__model='case', activity_type=Activity.ActivityChoices.UPVOTE, object_id=case.uuid).count(),
            Activity.objects.filter(content_type__model='case', activity_type=Activity.ActivityChoices.DOWNVOTE, object_id=case.uuid).count(),
            Activity.objects.filter(content_type__model='case', activity_type=Activity.ActivityChoices.VIEW, object_id=case.uuid).count()
        }
    except Exception:
        return [0, 0, 0, 0]
