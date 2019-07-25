from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

import datetime

from safe.models import Safe, Safe_Event
from .crypto import Crypto

crypto_handler = Crypto()

# Create your views here.
def register(request):
    public_key = crypto_handler.pub_key()
    valid_request = False
    now = datetime.datetime.now()
    if request.method =='GET':
        parms = request.GET
        if 'hwid' in parms and 'pkey' in parms:
            # Check if we have a safe with this id already
            try:
                safe = Safe.objects.get(
                    hardware_id=parms['hwid'],
                )
                created = False
            except Safe.DoesNotExist:
                safe = Safe(
                    hardware_id=parms['hwid'],
                    safe_public_key=parms['pkey'],
                    last_update=now,
                    unlock_time=now,
                    auth_to_unlock=True
                )
                created = True
            if created:
                print('New safe record created, {}'.format(safe.hardware_id))
            else:
                print('Safe record updated with public key, {}'.format(safe.hardware_id))
            safe.safe_public_key = parms['pkey']
            safe.last_update = now
            safe.save()
            valid_request = True
    if valid_request:
        return HttpResponse(public_key)
    else:
        return HttpResponse('Invalid request')


def checkin(request):
    valid_request = False
    safe_found = False
    now = datetime.datetime.now(datetime.timezone.utc)
    if request.method =='GET':
        parms = request.GET
        if 'hwid' in parms and 'sig' in parms and 'msg' in parms:
            # Check if we have a safe with this id already
            try:
                safe = Safe.objects.get(
                    hardware_id=parms['hwid'],
                )
                safe_found = True
            except Safe.DoesNotExist:
                pass
            if safe_found:
                msg_valid, message = crypto_handler.decrypt(msg=parms['msg'], sig=parms['sig'],
                                                            pkey=safe.safe_public_key)
            if msg_valid:
                valid_request = True
    if valid_request:
        # Interpret content and update database
        # Remember, message may be multiple lines
        if '\n' in message:
            message_lines = message.split('\n')
        else:
            message_lines = [message,]
        status_parts = message_lines[0].split(',')
        if len(status_parts) == 6:
            safe.last_update = status_parts[2]
            if status_parts[3] == 'True':
                safe.hinge_closed = True
            if status_parts[4] == 'True':
                safe.lid_closed = True
            if status_parts[5] == 'True':
                safe.bolt_engaged = True
            # Now check if there are any time-based updates to make
            if safe.unlock_time < now:
                safe.auth_to_unlock = True
            safe.save()
            if len(message_lines) > 1:
                # Add entries to Safe events database
                for i in range(len(message_lines)-1):
                    if message_lines[i+1].startswith('EVENT'):
                        event_parts = message_lines[i+1].split(',')
                        if len(event_parts) == 3:
                            event = Safe_Event.objects.create(safe=safe,
                                                                 event=event_parts[2],
                                                                 timestamp=event_parts[1])
        # Now construct a response, encrypt, sign and return it
        server_message_base = 'Auth_to_unlock:{}:{}\nUnlock_time:{}\nSettings:SCANFREQ={' \
                         '}:REPORTFREQ={}:PROXIMITYUNIT={}:DISPLAYPROXIMITY={}'
        if safe.auth_to_unlock:
            auth_msg = 'TRUE'
        else:
            auth_msg = 'FALSE'
        if safe.displayproximity:
            disp_msg = 'TRUE'
        else:
            disp_msg = 'FALSE'
        server_message = server_message_base.format(auth_msg, now, safe.unlock_time,
                                                    safe.scanfreq, safe.reportfreq,
                                                    safe.proximityunit, disp_msg)
        print('Returning message to safe:\n'.format(server_message))
        msg_enc_64, msg_sig_64 = crypto_handler.encrypt(msg=server_message,
                                                        safe_pkey=safe.safe_public_key)
        return HttpResponse(msg_enc_64 + b'***PART***' + msg_sig_64)
    else:
        return HttpResponse('Invalid request')

