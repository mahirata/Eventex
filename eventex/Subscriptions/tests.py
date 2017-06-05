from django.core import mail
from django.test import TestCase
from eventex.Subscriptions.forms import SubscriptionForm

class SubcribeTest(TestCase):
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
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """ Html must constain csrf """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have subscription form """
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """ Form must have 4 fields """
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Marco Hirata', cpf='12345678901', email='marco.hirata@gmail.com', phone='11-98730-0315')
        self.resp = self.client.post('/inscricao/', data)


    def test_post(self):
        """ Valid Post should redirect to /inscricao/ """
        self.assertEquals(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEquals(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEquals(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEquals(expect, email.from_email)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'marco.hirata@gmail.com']

        self.assertEquals(expect, email.to)

    def test_subscription_email_to(self):
        email = mail.outbox[0]

        self.assertIn('Marco Hirata', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('marco.hirata@gmail.com', email.body)
        self.assertIn('11-98730-0315', email.body)


class SubscriveInvalidPost(TestCase):
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


