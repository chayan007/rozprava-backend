from django.db.models import Avg

from activity.models import Activity

from debate.models import Debate, DebateImpactHit


def get_debate_metrics(debate: Debate):
    """Get debate activity metrics."""
    return [
        Activity.objects.filter(content_type=Debate, object_id=debate.id, activity_type=Activity.ActivityChoices.REPORT),
        Activity.objects.filter(content_type=Debate, object_id=debate.id, activity_type=Activity.ActivityChoices.UPVOTE),
        Activity.objects.filter(content_type=Debate, object_id=debate.id, activity_type=Activity.ActivityChoices.DOWNVOTE),
        Activity.objects.filter(content_type=Debate, object_id=debate.id, activity_type=Activity.ActivityChoices.VIEW)
    ]


def get_debate_impact(debate: Debate):
    """Get aggregate debate impact hit."""
    debate_summary = DebateImpactHit.objects.filter(
        debate=debate
    ).annotate(
        average_impact=Avg('impact')
    ).values(
        'average_impact'
    )
    return round(getattr(debate_summary, 'average_impact', 0))
