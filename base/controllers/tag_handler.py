from sentry_sdk import capture_exception

from activity.models import HashTag

from case.models import Case

from debate.models import Debate


class TagHandler:
    """Handle all tag functions."""

    @staticmethod
    def extract_tags(raw_string: str):
        """Extract all tag."""
        return set(
            part[1:]
            for part in raw_string.split()
            if part.startswith('#')
        )

    @staticmethod
    def increment_tags_count(tag_objs: [HashTag]):
        """Increment count of tag."""
        for tag_obj in tag_objs:
            tag_obj.views += 1
            tag_obj.save()

    @staticmethod
    def store_and_get_tag(tag: str):
        """Store all tags present in description."""
        return HashTag.objects.get_or_create(name=tag)

    def handle_tag_cycle(self, raw_string: str, indicator_uuid: str, indicator: str):
        """Handle all tags."""
        try:
            tags = self.extract_tags(raw_string)
            extracted_tags = []
            for tag in tags:
                extracted_tags.append(self.store_and_get_tag(tag))
            if indicator.lower() == 'case':
                Case.objects.get(uuid=indicator_uuid).tags.add(*extracted_tags)
            elif indicator.lower() == 'debate':
                Debate.objects.get(uuid=indicator_uuid).tags.add(*extracted_tags)
            return extracted_tags
        except BaseException:
            capture_exception()
            return False
