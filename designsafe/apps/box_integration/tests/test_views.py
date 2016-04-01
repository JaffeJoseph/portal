from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from boxsdk.object.user import User
from designsafe.apps.box_integration.models import BoxUserStreamPosition, BoxUserToken
import mock


class BoxInitializationTestCase(TestCase):
    fixtures = ['user-data.json']

    def setUp(self):
        # set password for users
        user = get_user_model().objects.get(pk=2)
        user.set_password('password')
        user.save()

    @mock.patch('designsafe.apps.auth.tasks.check_or_create_agave_home_dir.delay')
    def test_index_view_not_enabled(self, m_task):
        """
        Should render as not enabled
        """
        self.client.login(username='ds_user', password='password')
        m_task.assert_called_with('ds_user')

        response = self.client.get(reverse('box_integration:index'))
        self.assertContains(response, 'Box.com NOT Enabled')

    @mock.patch('designsafe.apps.auth.tasks.check_or_create_agave_home_dir.delay')
    def test_initialize_token_view(self, m_task):
        """
        Should respond with a 302 to Box OAuth
        """
        self.client.login(username='ds_user', password='password')
        m_task.assert_called_with('ds_user')

        response = self.client.get(reverse('box_integration:initialize_token'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('https://app.box.com/api/oauth2/authorize', response['Location'])

    @mock.patch('designsafe.apps.box_integration.tasks.initialize_box_sync.delay')
    @mock.patch('designsafe.apps.auth.tasks.check_or_create_agave_home_dir.delay')
    @mock.patch('boxsdk.object.events.Events.get_latest_stream_position')
    @mock.patch('boxsdk.object.user.User.get')
    @mock.patch('boxsdk.auth.oauth2.OAuth2.authenticate')
    def test_oauth2_callback(self, m_box_oauth_authenticate, m_user_get,
                             m_get_latest_stream_position,
                             m_check_or_create_agave_home_dir, m_initialize_box_sync):

        """
        Tests the Box OAuth2 Callback handler. After completing the OAuth auth code flow,
        the user has a BoxUserToken and BoxUserStreamPosition object and calls can be made
        to the Box API on the user's behalf.

        Args:
            m_box_oauth_authenticate: mock for boxsdk OAuth2.authenticate
            m_user_get: mock for boxsdk User.get
            m_get_latest_stream_position: mock for boxsdk
                                          Events.get_latest_stream_position
            m_check_or_create_agave_home_dir: mock for the check_or_create_agave_home_dir
                                              task
            m_initialize_box_sync: mock for the initialize_box_sync task
        """
        self.client.login(username='ds_user', password='password')
        m_check_or_create_agave_home_dir.assert_called_with('ds_user')

        session = self.client.session
        session['box'] = {
            'state': 'box_csrf_state_123'
        }
        session.save()

        # patch return_values
        m_box_oauth_authenticate.return_value = ('asdf', 'asdf1234')
        m_user_get.return_value = User(None, 'me', {
            'id': '100000000',
            'name': 'DS User',
            'login': 'ds_user@designsafe-ci.org'
        })
        m_get_latest_stream_position.return_value = 1234567890

        response = self.client.get(reverse('box_integration:oauth2_callback'),
                                   {'code': 'box_authorization_code_123',
                                    'state': 'box_csrf_state_123'
                                    })

        user = get_user_model().objects.get(username='ds_user')
        self.assertEqual('asdf', user.box_user_token.access_token)
        self.assertEqual('1234567890', user.box_stream_pos.stream_position)

        m_initialize_box_sync.assert_called_with('ds_user')

        self.assertRedirects(response, reverse('box_integration:index'),
                             fetch_redirect_response=False)

        response = self.client.get(reverse('box_integration:index'))
        self.assertContains(response, 'Box.com Enabled')
        self.assertContains(response,
                            'Box.com as <em>DS User (ds_user@designsafe-ci.org)</em>')


class BoxDisconnectTestCase(TestCase):
    fixtures = ['user-data.json', 'box-user-token.json', 'box-event-stream-position.json']

    def setUp(self):
        # set password for users
        user = get_user_model().objects.get(pk=2)
        user.set_password('password')
        user.save()

    @mock.patch('designsafe.apps.auth.tasks.check_or_create_agave_home_dir.delay')
    def test_disconnect(self, m_check_or_create_agave_home_dir):
        """
        Test disconnecting Box.com.

        Args:
            m_check_or_create_agave_home_dir: mock for the check_or_create_agave_home_dir
                                              task
        """
        # log the test user in
        self.client.login(username='ds_user', password='password')
        m_check_or_create_agave_home_dir.assert_called_with('ds_user')

        # verify we have preconditions
        user = get_user_model().objects.get(username='ds_user')
        self.assertIsNotNone(user.box_user_token)
        self.assertIsNotNone(user.box_stream_pos)

        # verify we can render the view
        response = self.client.get(reverse('box_integration:disconnect'))
        self.assertEqual(response.status_code, 200)

        # confirm disconnect request
        response = self.client.post(reverse('box_integration:disconnect'))

        self.assertRedirects(response, reverse('box_integration:index'),
                             fetch_redirect_response=False)

        # verify related objects were deleted
        self.assertRaises(BoxUserToken.DoesNotExist, BoxUserToken.objects.get, user=user)
        self.assertRaises(BoxUserStreamPosition.DoesNotExist,
                          BoxUserStreamPosition.objects.get, user=user)
