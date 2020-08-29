import json
import pprint

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from sms_messenger.common.models import SMS, MMS


@csrf_exempt
def messages(request):
    if request.method == 'POST':
        msg_dct = json.loads(request.body)
        pprint.pprint(msg_dct)
        
        msg_class = MMS if msg_dct['data']['attributes']['is_mms'] else SMS
        
        msg = msg_class()
        msg.update_from_dict(msg_dct)
        msg.save()
        
    return HttpResponse('HERE!!')
