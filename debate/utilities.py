from activity.models import Activity

from debate.models import Debate


def get_debate_metrics(debate: Debate):
    """Get debate activity metrics."""
    try:
        return [
            Activity.objects.filter(content_object=debate, activity_type=Activity.ActivityChoices.REPORT),
            Activity.objects.filter(content_object=debate, activity_type=Activity.ActivityChoices.UPVOTE),
            Activity.objects.filter(content_object=debate, activity_type=Activity.ActivityChoices.DOWNVOTE),
            Activity.objects.filter(content_object=debate, activity_type=Activity.ActivityChoices.VIEW)
        ]
    except Exception:
        # TODO: Solve this query.
        return [0, 0, 0, 0]
