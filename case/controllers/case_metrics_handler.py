from activity.models import Activity
from case.models import Case


class CaseMetrics:

    def __init__(self, case_id: str):
        self.case = Case.objects.get(case_id)

    def like_or_unlike(self, user):
        try:
            Activity.objects.get(
                content_object=self.case,
                activity_type=Activity.ActivityChoices.LIKE,
                profile=user.profile
            ).delete()
        except Activity.DoesNotExist:
            Activity.objects.create(
                content_object=self.case,
                activity_type=Activity.ActivityChoices.LIKE,
                profile=user.profile
            )

    def report(self, user):
        try:
            Activity.objects.get(
                content_object=self.case,
                activity_type=Activity.ActivityChoices.REPORT,
                profile=user.profile
            ).delete()
        except Activity.DoesNotExist:
            Activity.objects.create(
                content_object=self.case,
                activity_type=Activity.ActivityChoices.REPORT,
                profile=user.profile
            )

    def get_metrics(self):
        return {
            'likes': self.case.activities.filter(
                activity_type=Activity.ActivityChoices.LIKE
            ).count(),
            'reports': self.case.activities.filter(
                activity_type=Activity.ActivityChoices.REPORT
            ).count()
        }