from activity.models import Activity

from case.models import Case


def get_case_metrics(case: Case):
    """Get case activity metrics."""
    try:
        case_activity = Activity.objects.filter(content_type__model='case', object_id=case.uuid)
        return {
            case_activity.filter(activity_type=Activity.ActivityChoices.REPORT).count() or 0,
            case_activity.filter(activity_type=Activity.ActivityChoices.UPVOTE).count() or 0,
            case_activity.filter(activity_type=Activity.ActivityChoices.DOWNVOTE).count() or 0,
            case_activity.filter(activity_type=Activity.ActivityChoices.VIEW).count() or 0
        }
    except Exception:
        return [0, 0, 0, 0]
