from rest_framework import serializers

from sms_messenger.common.models import SMS, MMS


class SMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMS
        fields = ('id', 'from_number', 'to_number', 'is_inbound', 'body', 'timestamp', 'status', 'last_modified')


class MMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = MMS
        fields = ('id', 'from_number', 'to_number', 'is_inbound', 'body', 'timestamp', 'status', 'last_modified')
