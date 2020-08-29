from django.contrib import admin

from sms_messenger.common.models import SMS, MMS


admin.site.register(SMS)
admin.site.register(MMS)
