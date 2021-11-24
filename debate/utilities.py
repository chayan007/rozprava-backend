from activity.models import Activity

from debate.models import Debate


def get_debate_metrics(debate: Debate):
    """Get debate activity metrics."""
    try:
        debate_activity = Activity.objects.filter(content_type__model='debate', object_id=debate.uuid)
        return [
            debate_activity.filter(activity_type=Activity.ActivityChoices.REPORT).count() or 0,
            debate_activity.filter(activity_type=Activity.ActivityChoices.UPVOTE).count() or 0,
            debate_activity.filter(activity_type=Activity.ActivityChoices.DOWNVOTE).count() or 0,
            debate_activity.filter(activity_type=Activity.ActivityChoices.VIEW).count() or 0
        ]
    except Exception:
        return [0, 0, 0, 0]
