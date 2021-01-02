from activity.models import Tag

from case.models import Case

from debate.models import Debate


class TagHandler:
    """Handle all tag functions."""

    @staticmethod
    def extract_tags(raw_string):
        """Extract all tag."""
        return set(
            part[1:]
            for part in raw_string.split()
            if part.startswith('#')
        )

    @staticmethod
    def increment_tags_count(tag_objs):
        """Increment count of tag."""
        for tag_obj in tag_objs:
            tag_obj.views += 1
            tag_obj.save()

    @staticmethod
    def store_and_get_tag(tag):
        """Store all tags present in description."""
        try:
            return Tag.objects.create(name=tag)
        except BaseException:
            return Tag.objects.get(name=tag)

    def handle_tag_cycle(self, raw_string, indicator_uuid, indicator):
        """Handle all tags."""
        try:
            tags = self.extract_tags(raw_string)
            extracted_tags = []
            for tag in tags:
                extracted_tags.append(self.store_and_get_tag(tag))
            if indicator.lower() == 'case':
                Case.objects.get(uuid=indicator_uuid).tags(*extracted_tags)
            elif indicator.lower() == 'debate':
                Debate.objects.get(uuid=indicator_uuid).tags(*extracted_tags)
            return extracted_tags
        except BaseException as e:
            return False
