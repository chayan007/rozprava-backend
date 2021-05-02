from activity.models import Activity

from debate.models import Debate


def get_debate_metrics(debate: Debate):
    """Get debate activity metrics."""
    return [
        Activity.objects.filter(content_type=Debate, object_id=debate.id, activity_type=Activity.ActivityChoices.REPORT),
        Activity.objects.filter(content_type=Debate, object_id=debate.id, activity_type=Activity.ActivityChoices.UPVOTE),
        Activity.objects.filter(content_type=Debate, object_id=debate.id, activity_type=Activity.ActivityChoices.DOWNVOTE),
        Activity.objects.filter(content_type=Debate, object_id=debate.id, activity_type=Activity.ActivityChoices.VIEW)
    ]
