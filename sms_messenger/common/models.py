import datetime

from django.db import models


class SMS(models.Model):
    id = models.CharField(max_length=37, primary_key=True)
    from_number = models.CharField(max_length=32)
    to_number = models.CharField(max_length=32)
    is_inbound = models.BooleanField()
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=32, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def update_from_dict(self, msg_dct):
        self.id = msg_dct['data']['id']
        self.from_number = msg_dct['data']['attributes']['from']
        self.to_number = msg_dct['data']['attributes']['to']
        self.is_inbound = msg_dct['data']['attributes']['direction'] == 'inbound'
        self.body = msg_dct['data']['attributes']['body']
        self.timestamp = datetime.datetime.strptime(msg_dct['data']['attributes']['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)  # "2019-06-04T15:29:14.32Z"
        self.status = msg_dct['data']['attributes']['status']
        
        return self


class MMS(SMS):
    def update_from_dict(self, msg_dct):
        super().update_from_dict(msg_dct)
        return self
