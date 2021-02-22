from django.db import DataError, IntegrityError

from activity.models import Activity

from debate.models import Debate

from profiles.models import User


class DebateMetrics:

    def __init__(self, debate_uuid: str = None):
        if debate_uuid:
            self.debate = Debate.objects.get(uuid=debate_uuid)

    @staticmethod
    def increment_views(debate_uuids: [str], user: User) -> None:
        for debate_uuid in debate_uuids:
            try:
                debate = Debate.objects.get(uuid=debate_uuid)
                debate.activities.create(
                    activity_type=Activity.ActivityChoices.VIEW,
                    profile=user.profile
                )
            except (DataError, IntegrityError):
                continue

    def like_or_unlike(self, user: User) -> None:
        try:
            Activity.objects.get(
                content_object=self.debate,
                activity_type=Activity.ActivityChoices.UPVOTE,
                profile=user.profile
            ).delete()
        except Activity.DoesNotExist:
            Activity.objects.create(
                content_object=self.debate,
                activity_type=Activity.ActivityChoices.UPVOTE,
                profile=user.profile
            )

    def report_or_unreport(self, user: User) -> None:
        try:
            Activity.objects.get(
                content_object=self.debate,
                activity_type=Activity.ActivityChoices.REPORT,
                profile=user.profile
            ).delete()
        except Activity.DoesNotExist:
            Activity.objects.create(
                content_object=self.debate,
                activity_type=Activity.ActivityChoices.REPORT,
                profile=user.profile
            )

    def get_metrics_for_debate(self) -> dict:
        return {
            'likes': self.debate.activities.filter(
                activity_type=Activity.ActivityChoices.UPVOTE
            ).count(),
            'reports': self.debate.activities.filter(
                activity_type=Activity.ActivityChoices.REPORT
            ).count(),
            'views': self.debate.activities.filter(
                activity_type=Activity.ActivityChoices.VIEW
            ).count()
        }
