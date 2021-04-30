from django.contrib import admin

from verification.models import KYCVerification, OTPVerification

admin.site.register(KYCVerification)
admin.site.register(OTPVerification)
