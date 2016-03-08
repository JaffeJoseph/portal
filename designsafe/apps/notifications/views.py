# from designsafe.apps.notifications.tasks import send_job_notification
from designsafe.apps.notifications.apps import Event
from designsafe.apps.signals.signals import generic_event
from designsafe.apps.notifications.models import Notification
from designsafe.apps.signals.signals import generic_event

from django.core import serializers
# from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from agavepy.agave import Agave, AgaveException
from django.conf import settings
from django.contrib.auth import get_user_model

import json
import logging


logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'designsafe/apps/notifications/index.html')


@require_POST
@csrf_exempt
def generic_webhook_handler(request):
    if request.method == 'POST':
        # do stuff
        event_type = request.POST.get('event_type', None)
    else:
        # do other stuff, to be determined in future webhooks I suppose
        return HttpResponse('Unexpected', status=400)

    if event_type == 'VNC':
        event_type = request.POST.get('event_type', '')
        job_owner = request.POST.get('owner', '')
        host = request.POST.get('host', '')
        port = request.POST.get('port','')
        password = request.POST.get('password','')
        job_uuid = password

        body = {
            'event_type': event_type,
            'job_owner': job_owner,
            'host': host,
            'port': port,
            'password': password,
            'associationIds': job_uuid,
        }
        generic_event.send_robust('generic_webhook_handler', event_type=event_type, event_data=body)

        # create metadata for VNC connection and save to agave metadata?
        try:
            agave_job_meta = {
                'name':'interactiveJobDetails',
                'value': body,
                'associationIds': [job_uuid],
            }
            logger.info('refreshing for user={}'.format(job_owner))
            user = get_user_model().objects.get(username=job_owner)
            token = user.agave_oauth
            if token.expired:
                token.refresh()
            agave = Agave(api_server=settings.AGAVE_TENANT_BASEURL, token=token.access_token)
            logger.info('token.access_token={}'.format(token.access_token))
            logger.info('SENDING BODY={}'.format(agave_job_meta))
            meta_uuid = agave.meta.addMetadata(body=json.dumps(agave_job_meta))
            logger.info('JOB NOTIFICATION agave meta response: {}'.format(meta_uuid))


        except AgaveException as e:
            logger.info('AGAVE EXCEPTION {}'.format(e))
            return HttpResponse(json.dumps(e.message), content_type='application/json',
                status=400)
        except Exception as e:
            logger.exception('EXCEPTION BOO! {}'.format(e))

        return HttpResponse('OK')
    else:
        return HttpResponse('Unexpected', status=400)

@require_POST
@csrf_exempt
def job_notification_handler(request):
    JOB_EVENT='job'
    logger.debug('request body: {}'.format(request.body))

    try:
        notification = json.loads(request.body)
        logger.info('notification body: {}'.format(notification))
        logger.info('notification name: {}'.format(notification['name']))
        job_name = notification['name']
        status = notification['status']
        event = request.GET.get('event')
        job_id = request.GET.get('job_id')
        job_owner = notification['owner']
        archive_path = notification['archivePath']
    except ValueError as e: #for testing ->used when mocking agave notification
        job_name = request.POST.get('job_name')
        status = request.POST.get('status')
        event = request.POST.get('event')
        job_id = request.POST.get('job_id')
        job_owner = request.POST.get('job_owner')
        archive_path = request.POST.get('archivePath')

    logger.info('job_name: {}'.format(job_name))
    logger.info('event: {}'.format(event))
    logger.info('job_id: {}'.format(job_id))

    body = {
        'job_name': job_name,
        'job_id': job_id,
        'event': event,
        'status': status,
        'archive_path': archive_path,
        'job_owner': job_owner,
    }
    generic_event.send_robust(None, event_type='job', event_data=body,
                             event_users=[job_owner])

    return HttpResponse('OK')


def get_number_unread_notifications(request):
    # nondeleted = JobNotification.objects.filter(deleted=False, user=str(request.user)).count()
    unread = Notification.objects.filter(deleted=False, read=False, user=str(request.user)).count()
    # logger.info('nondeleted: {}'.format(nondeleted))
    logger.info('unread: {}'.format(unread))
    return unread


def notifications(request):
    items = Notification.objects.filter(
        deleted=False,
        user=str(request.user)).order_by('-notification_time')
    unread = 0
    for i in items:
        if not i.read:
            unread += 1
            i.mark_read()
    try:
        items = serializers.serialize('json', items)
    except TypeError as e:
        items=[]
    return HttpResponse(items, content_type='application/json')


def delete_notification(request):
    body = json.loads(request.body)
    pk = body['pk']
    logger.info('pk: {}'.format(pk))
    if pk == 'all':
        items=Notification.objects.filter(deleted=False, user=str(request.user))
        for i in items:
            i.mark_deleted()
    else:
        x = Notification.objects.get(pk=pk)
        x.mark_deleted()

    return HttpResponse('OK')
