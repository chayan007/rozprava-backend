from activity.models import Activity

from debate.models import Debate


def get_debate_metrics(debate: Debate):
    """Get debate activity metrics."""
    try:
        return [
            Activity.objects.filter(content_type__model='debate', activity_type=Activity.ActivityChoices.REPORT, object_id=debate.uuid),
            Activity.objects.filter(content_type__model='debate', activity_type=Activity.ActivityChoices.UPVOTE, object_id=debate.uuid),
            Activity.objects.filter(content_type__model='debate', activity_type=Activity.ActivityChoices.DOWNVOTE, object_id=debate.uuid),
            Activity.objects.filter(content_type__model='debate', activity_type=Activity.ActivityChoices.VIEW, object_id=debate.uuid)
        ]
    except Exception:
        return [0, 0, 0, 0]
