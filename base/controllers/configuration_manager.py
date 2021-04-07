import json
from glob import glob

from base.models import Configuration


class ConfigurationManager:

    def __init__(self):
        self.config_paths = self._list_from_config_folder()

    @staticmethod
    def _list_from_config_folder():
        """Return list of config paths."""
        return glob('base/config/*.json')

    def parse_and_load_to_config(self):
        """Parse and upload config to database."""
        for config_path in self.config_paths:
            configurations = json.load(open(config_path))

            if not configurations:
                continue

            for configuration in configurations:
                name = configuration.get('name')
                key = configuration.get('key')
                value = configuration.get('value', {})

                Configuration.objects.update_or_create(
                    key=key,
                    defaults={
                        'name': name,
                        'value': value
                    }
                )
