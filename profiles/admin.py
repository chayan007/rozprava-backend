from django.contrib import admin

from profiles.models import FollowerMap, Group, Profile

admin.site.register(Profile)
admin.site.register(FollowerMap)
admin.site.register(Group)
