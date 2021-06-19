from django.core.management.base import BaseCommand

from base.controllers.configuration_manager import ConfigurationManager


class Command(BaseCommand):

    help = 'Manages configuration model for Rozprava'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--refresh',
            action='store_true',
            help='Refresh Configuration Model',
        )

    def handle(self, *args, **kwargs):
        reset_flag = kwargs.get('refresh', False)
        ConfigurationManager().parse_and_load_to_config(reset_flag)
        self.stdout.write(
            f"Configurations have been {'refreshed with empty values' if reset_flag else 'set with default values'}."
        )
