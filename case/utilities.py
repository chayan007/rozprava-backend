from activity.models import Activity

from case.models import Case


def get_case_metrics(case: Case):
    """Get case activity metrics."""
    try:
        return [
            Activity.objects.filter(content_object=case, activity_type=Activity.ActivityChoices.REPORT),
            Activity.objects.filter(content_object=case, activity_type=Activity.ActivityChoices.UPVOTE),
            Activity.objects.filter(content_object=case, activity_type=Activity.ActivityChoices.DOWNVOTE),
            Activity.objects.filter(content_object=case, activity_type=Activity.ActivityChoices.VIEW)
        ]
    except Exception:
        # TODO: Solve this query.
        return [0, 0, 0, 0]
