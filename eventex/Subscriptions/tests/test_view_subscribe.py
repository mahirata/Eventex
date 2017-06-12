from django.core import mail
from django.test import TestCase
from eventex.Subscriptions.forms import SubscriptionForm

class SubcribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """ Get /inscricao/ must return status code 200 """
        self.assertEquals(200, self.resp.status_code)

    def test_template(self):
        """ Must use Subscriptions/subscriptions_form.thml """
        self.assertTemplateUsed(self.resp, 'Subscriptions/subscription_form.html')

    def test_html(self):
        """ html must contain inputs tags """
        tags = (('<form', 1),
               ('<input', 6),
               ('type="text"', 3),
               ('type="email"', 1),
               ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """ Html must constain csrf """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have subscription form """
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Marco Hirata', cpf='12345678901', email='marco.hirata@gmail.com', phone='11-98730-0315')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """ Valid Post should redirect to /inscricao/ """
        self.assertEquals(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEquals(1, len(mail.outbox))


class SubscrivePostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """ Invalid POST should not redirect """
        self.assertEquals(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'Subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMassage(TestCase):
    def test_message(self):
        data = dict(name='Marco Hirata', cpf='12345678901',
                    email='marco.hirata@mailinator.com', phone='11-98730-0315')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')


