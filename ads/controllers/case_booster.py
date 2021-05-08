import datetime

from ads.exceptions import BoostFailedException
from ads.models import Boost

from base.constants import UNIQUE_DATE_FORMAT
from base.controllers.configuration_manager import ConfigurationManager

from case.models import Case

from profiles.exceptions import UserValidationFailedException
from profiles.models import Profile


class CaseBooster:
    """Boost case for popularity."""

    def __init__(self, profile: Profile):
        self.profile = profile

    def create(self, **kwargs):
        """Create a case boost request."""
        total_amount = kwargs['amount']
        start_date = datetime.datetime.strptime(kwargs['start_date'], UNIQUE_DATE_FORMAT)
        end_date = datetime.datetime.strptime(kwargs['end_date'], UNIQUE_DATE_FORMAT)

        number_of_days = (end_date - start_date).days
        per_day_amount_allotment = total_amount / number_of_days

        minimum_per_day_amount_allotment = ConfigurationManager.get('MINIMUM_PER_DAY_AMOUNT_ALLOTMENT')

        if per_day_amount_allotment < minimum_per_day_amount_allotment:
            raise BoostFailedException(
                f'Minimum per day boost allocation must be INR {minimum_per_day_amount_allotment} '
                f'whereas your per day boost allocation is INR {per_day_amount_allotment}.'
            )

        Boost.records.create(
            profile=self.profile,
            case=Case.objects.get(kwargs['case_uuid']),
            amount=total_amount,
            per_day_allotment=per_day_amount_allotment,
            start_date=start_date,
            end_date=end_date
        )

    def update(self, boost_uuid: str, **kwargs):
        """
        Following updates are only allowed.

        1. Increasing ad budget i.e. `total_amount`
        2. Extending `end_date` timeline for ad
        """
        boost = Boost.objects.get(uuid=boost_uuid)

        if boost.profile != self.profile:
            raise UserValidationFailedException(
                f'{self.profile.user.username} has no rights over this advertisement.'
            )

        if kwargs.get('additional_amount'):
            boost.total_amount += kwargs.get('additional_amount')

        if kwargs.get('end_date'):
            end_date = datetime.datetime.strptime(kwargs['end_date'], UNIQUE_DATE_FORMAT)
            assert end_date > boost.end_date
            boost.end_date = end_date

        adjusting_amount = kwargs.get('additional_amount', 0)
        remaining_days = (boost.end_date - boost.start_date).days

        boost.per_day_allotment = (boost.per_day_allotment * remaining_days) + adjusting_amount / remaining_days
        boost.save()
