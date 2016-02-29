from django.conf.urls import include, url, patterns
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


urlpatterns = patterns('designsafe.apps.notifications.views',
    url(r'^$', 'index', name='index'),
    url(r'^jobs/$', 'job_notification_handler', name='job_notification_handler'),
    url(r'^notifications/$', 'notifications', name='notifications'),
    url(r'^delete/$', 'delete_notification', name='delete_notification'),

    # url(r'^apps-list/$', 'apps_list', name='apps_list'),
    # url(r'^files-list/$', 'files_list', name='files_list'),
    # url(r'^jobs-list/$', 'jobs_list', name='jobs_list'),
    # url(r'^jobs-details/$', 'jobs_details', name='jobs_details'),
)


def menu_items(**kwargs):
    if 'type' in kwargs and kwargs['type'] == 'account':
        return [
            {
                'label': _('Notifications'),
                'url': reverse('designsafe_notifications:index'),
                'children': []
            }
        ]
