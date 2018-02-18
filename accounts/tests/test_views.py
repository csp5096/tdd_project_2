from django.test import TestCase
from unittest.mock import patch, call
import accounts.views

class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        self.assertRedirects(response, '/')

    def test_sends_mail_to_address_from_post(self):
        self.send_mail_called = False

    def fake_send_mail(self, subject, body, from_email, to_list):
        self.send_mail_called = True
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to_list = to_list
        accounts.views.send_email = fake_send_mail
        self.client.post('/accounts/send_login_email',
                         data={'email': 'edith@example.com'
        })
        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for Superlists')
        self.assertEqual(self.from_email, 'noreply@superlists')
        self.assertEqual(self.to_list, ['edith@example.com'])

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email',
                         data={'email': 'edith@example.com'
        })
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email',
                         data={'email': 'edith@example.com'
                               }, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(message.message,
                         "Check your email, we've sent you a link you can use to log in."
                         )
        self.assertEqual(message.tags, "success")

    @patch('accounts.views.messages')
    def test_add_success_message_with_mocks(self, mock_messages):
        response = self.client.post('/accounts/send_login_email',
                         data={'email': 'edith@example.com'
        })
        expected = "Check your email, we've sent you a link you can use to log in."
        self.assertEqual(mock_messages.success.call_args,
                         call(response.wsgi_request, expected),
                         )