from rest_framework import serializers

from activity.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    activity = serializers.SerializerMethodField()

    def get_activity(self, obj):
        return obj.get_activity_type_display()

    class Meta:
        model = Activity
        fields = (
            'activity',
            'content_type',
            'content_object'
        )
