from django.db import DataError, IntegrityError

from activity.models import Activity

from case.models import Case

from profiles.models import User


class CaseMetrics:

    def __init__(self, case_uuid: str = None):
        if case_uuid:
            self.case = Case.objects.get(uuid=case_uuid)

    @staticmethod
    def increment_views(case_uuids: [str], user: User) -> None:
        for case_uuid in case_uuids:
            try:
                case = Case.objects.get(uuid=case_uuid)
                case.activities.create(
                    activity_type=Activity.ActivityChoices.VIEW,
                    profile=user.profile
                )
            except (DataError, IntegrityError):
                continue

    def like_or_unlike(self, user: User) -> None:
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

    def report_or_unreport(self, user: User) -> None:
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

    def get_metrics_for_case(self) -> dict:
        return {
            'likes': self.case.activities.filter(
                activity_type=Activity.ActivityChoices.LIKE
            ).count(),
            'reports': self.case.activities.filter(
                activity_type=Activity.ActivityChoices.REPORT
            ).count(),
            'views': self.case.activities.filter(
                activity_type=Activity.ActivityChoices.VIEW
            ).count()
        }
