from django.contrib import admin

from profiles.models import FollowerMap, IdentityDocument, Group, Profile


admin.site.register(Profile)
admin.site.register(FollowerMap)
admin.site.register(IdentityDocument)
admin.site.register(Group)
