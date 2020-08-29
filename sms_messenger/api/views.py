import os
import sys
import sms_messenger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sms_messenger.__file__), os.pardir, 'libs', 'flowroute-sdk-v3-python')))

import io

from flowroutenumbersandmessaging.flowroutenumbersandmessaging_client import FlowroutenumbersandmessagingClient

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from sms_messenger.common.models import SMS, MMS

from .serializers import SMSSerializer, MMSSerializer

FR_BASIC_AUTH_USERNAME = input('Flowroute secret key: ')
FR_BASIC_AUTH_PASSWORD = input('Flowroute secret password: ')


@csrf_exempt
def messages(request):
    if request.method == 'GET':
        sms_queryset = SMS.objects.filter(mms=None)
        mms_queryset = MMS.objects.all()
        
        sms_serializer = SMSSerializer(sms_queryset, many=True)
        mms_serializer = MMSSerializer(mms_queryset, many=True)
        
        sms_data = sms_serializer.data
        mms_data = mms_serializer.data
        
        msg_data = sms_data + mms_data
        msg_json = JSONRenderer().render(msg_data)
        
        return HttpResponse(msg_json)
    
    if request.method == 'POST':
        body_stream = io.BytesIO(request.body)
        msg_data = JSONParser().parse(body_stream)
        
        fr_msg_data = {
            'data': {
                'type': 'message',
                'attributes': {
                    'from': msg_data['from_number'],
                    'to': msg_data['to_number'],
                    'body': msg_data['body'],
                    'is_mms': msg_data['is_mms'],
                },
            },
        }
        fr_msg_json = JSONRenderer().render(fr_msg_data)
        
        fr_client = FlowroutenumbersandmessagingClient(FR_BASIC_AUTH_USERNAME, FR_BASIC_AUTH_PASSWORD)
        fr_msg_ctl = fr_client.messages
        
        fr_result_data = fr_msg_ctl.send_a_message(fr_msg_json)
        fr_result_json = JSONRenderer().render(fr_result_data)
        
        return HttpResponse(fr_result_json)
